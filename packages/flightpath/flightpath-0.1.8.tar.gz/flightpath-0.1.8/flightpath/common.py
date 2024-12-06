import duckdb
import logging


def find_final_task(duckdb_location: str, dag_run_id: str) -> tuple[str, str]:
    with duckdb.connect(duckdb_location) as conn:
        result = conn.execute("""
            SELECT dag_id, task_id
            FROM task_instances
            WHERE dag_run_id = ?
            AND end_date IS NOT NULL
            ORDER BY end_date DESC
            LIMIT 1
        """, [dag_run_id]).fetchone()

        if not result:
            raise ValueError(f"No completed tasks found for dag_run_id: {dag_run_id}")
            
        return result[0], result[1]
        


def calculate_critical_path(
    end_task_id: str, end_dag_id: str, dag_run_id: str, duckdb_location: str
) -> list[str]:
    """Trace a critical path from a specific task, potentially across multiple DAGs."""

    logging.info("Extracting critical path...")

    output = []

    with duckdb.connect(duckdb_location) as conn:
        # Check if the task_id and dag_id exist in the task_instances table for the given dag_run_id
        check_query = """
        SELECT COUNT(*) as count
        FROM task_instances
        WHERE task_id = ? AND dag_id = ? AND dag_run_id = ?
        """
        result = conn.execute(
            check_query, [end_task_id, end_dag_id, dag_run_id]
        ).fetchone()

        if result[0] == 0:
            conn.close()
            raise ValueError(
                f"No task instance found for specified starting point: task_id '{end_task_id}', dag_id '{end_dag_id}', and dag_run_id '{dag_run_id}'"
            )

        # Update the critical_path table schema
        conn.execute("DROP TABLE IF EXISTS critical_path")
        conn.execute("""
        CREATE TABLE critical_path (
            dag_id VARCHAR,
            dag_run_id VARCHAR,
            task_id VARCHAR,
            path_index INTEGER,
            ready_date TIMESTAMP,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            ready_seconds DECIMAL(9,2),
            running_seconds DECIMAL(9,2),
            total_seconds DECIMAL(9,2)
        )
        """)

        query = """
        WITH RECURSIVE critical_path_cte AS (
            SELECT 
                ti.task_id, 
                ti.dag_id,
                ti.start_date, 
                ti.end_date, 
                0 AS path_index
            FROM task_instances ti
            WHERE ti.task_id = ? AND ti.dag_id = ? AND ti.dag_run_id = ?
            
            UNION ALL
            
            SELECT 
                ti_upstream.task_id, 
                ti_upstream.dag_id,
                ti_upstream.start_date, 
                ti_upstream.end_date, 
                cp.path_index + 1 AS path_index
            FROM critical_path_cte cp
            JOIN dependencies d ON d.downstream_task_id = cp.task_id AND d.downstream_dag_id = cp.dag_id
            JOIN task_instances ti_upstream ON ti_upstream.task_id = d.upstream_task_id AND ti_upstream.dag_id = d.upstream_dag_id
            WHERE concat(ti_upstream.dag_id, '.', ti_upstream.task_id) = (
                SELECT concat(ti_upstream2.dag_id, '.', ti_upstream2.task_id)
                FROM task_instances ti_upstream2
                JOIN dependencies d2 ON d2.upstream_task_id = ti_upstream2.task_id AND d2.upstream_dag_id = ti_upstream2.dag_id
                WHERE d2.downstream_task_id = cp.task_id AND d2.downstream_dag_id = cp.dag_id
                AND ti_upstream2.dag_run_id = ?
                ORDER BY ti_upstream2.end_date DESC
                LIMIT 1
            )
            AND ti_upstream.dag_run_id = ?
        ),

        max_path_index AS (
            SELECT MAX(path_index) AS max_index FROM critical_path_cte
        ),

        final AS (
            SELECT 
                cp.dag_id,
                ? AS dag_run_id,
                cp.task_id,
                mpi.max_index - cp.path_index AS path_index,
                lead(cp.end_date) over (order by cp.path_index) as ready_date,
                cp.start_date, 
                cp.end_date,
                ifnull(date_diff('millisecond', lead(cp.end_date) over (order by cp.path_index), cp.start_date) / 1000, 0) as ready_seconds,
                date_diff('millisecond', cp.start_date, cp.end_date) / 1000 as running_seconds,
                ifnull(
                date_diff('millisecond', lead(cp.end_date) over (order by cp.path_index), cp.end_date) / 1000,
                date_diff('millisecond', cp.start_date, cp.end_date) / 1000
                ) as total_seconds
            FROM critical_path_cte cp
            CROSS JOIN max_path_index mpi
            ORDER BY path_index ASC
        )

        SELECT
        *
        FROM final
        """

        # Insert results into the critical_path table
        conn.execute(
            f"""
        INSERT INTO critical_path (dag_id, dag_run_id, task_id, path_index, ready_date, start_date, end_date, ready_seconds, running_seconds, total_seconds)
        {query}
        """,
            [end_task_id, end_dag_id, dag_run_id, dag_run_id, dag_run_id, dag_run_id],
        )

        # Fetch results for printing
        results = conn.execute(
            """
        SELECT dag_id, path_index, task_id, ready_date, start_date, end_date, ready_seconds, running_seconds, total_seconds
        FROM critical_path
        WHERE dag_run_id = ?
        ORDER BY path_index ASC
        """,
            [dag_run_id],
        ).fetchall()

        # Prepare data for printing
        headers = [
            "DAG ID",
            "Path Index",
            "Task ID",
            "Ready Date",
            "Start Date",
            "End Date",
            "Ready (Seconds)",
            "Running (Seconds)",
            "Total (Seconds)",
        ]
        data = [[str(item) for item in row] for row in results]
        all_rows = [headers] + data

        # Calculate column widths
        col_widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]

        # Create format string
        format_string = " | ".join("{:<" + str(width) + "}" for width in col_widths)

        output.append(format_string.format(*headers))
        output.append("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        for row in data:
            output.append(format_string.format(*row))

        # Calculate summary statistics
        summary_stats = conn.execute(
            """
        WITH base_stats AS (
            SELECT 
                SUM(ready_seconds) as total_ready,
                SUM(running_seconds) as total_running,
                SUM(total_seconds) as total_time,
                MAX(total_seconds) as max_total_time
            FROM critical_path
            WHERE dag_run_id = ?
        ),
        longest_task AS (
            SELECT dag_id, task_id
            FROM critical_path
            WHERE dag_run_id = ?
            AND total_seconds = (SELECT max_total_time FROM base_stats)
            LIMIT 1
        )
        SELECT 
            total_ready,
            total_running,
            total_time,
            (SELECT concat(dag_id, ':', task_id) FROM longest_task) as longest_task,
            max_total_time,
            ROUND(max_total_time * 100.0 / total_time, 1) as longest_task_percent
        FROM base_stats
        """,
            [dag_run_id, dag_run_id],
        ).fetchone()

        output.append("\n-- Statistics --")
        output.append(f"Ready Time:\t{summary_stats[0]:.1f} Seconds")
        output.append(f"Running Time:\t{summary_stats[1]:.1f} Seconds")
        output.append(f"Total Time:\t{summary_stats[2]:.1f} Seconds")
        output.append(
            f"Longest Task:\t{summary_stats[3]} ({summary_stats[4]} Seconds, {summary_stats[5]}% of total time)"
        )

        output.append("\n-- Parameters --")
        output.append(f"Run Id:\t\t{dag_run_id}")
        output.append(f"End Dag:\t{end_dag_id}")
        output.append(f"End Task:\t{end_task_id}")

    return output
