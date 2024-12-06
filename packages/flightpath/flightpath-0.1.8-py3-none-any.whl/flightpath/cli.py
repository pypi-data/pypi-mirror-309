#!/usr/bin/env python3

from requests.auth import HTTPBasicAuth
import logging
import getpass
import click
import os
import re

from flightpath.airflow import etl_dependencies, etl_task_instances, get_all_dag_ids
from flightpath.common import calculate_critical_path, find_final_task


# Updated CLI commands
@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.option(
    "-p",
    "--page-length",
    type=int,
    required=False,
    default=100,
    help="Page length for API calls (integer)",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, page_length: int) -> None:
    """Extract information from an Airflow instance."""
    if verbose:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    ctx.obj = {"page_length": page_length}


@cli.command()
@click.option("-u", "--username", type=str, help="Airflow username")
@click.option("-p", "--password", type=str, help="Airflow password")
@click.option("--baseurl", required=True, help="Base URL of the Airflow instance")
@click.option("--end-task-id", help="ID of the end task")
@click.option(
    "--end-dag-id",
    help="ID of the end DAG. If not provided, all DAGs will be extracted.",
)
@click.option("--dag-run-id", required=True, help="ID of the DAG run")
@click.option(
    "--dag-ids-to-trace",
    type=str,
    required=False,
    help="Comma-separated string of dag_ids to trace",
)
@click.option(
    "--dag-ids-to-trace-regex",
    type=str,
    required=False,
    help="Comma-separated list of regexes for dag_ids to trace",
)
@click.option(
    "-o", "--output", type=click.Path(), required=True, help="Output DuckDB file path"
)
@click.option(
    "--delete-db", is_flag=True, help="Delete existing duckdb db and generate new one"
)
@click.option(
    "--stay-within-dag",
    is_flag=True,
    help="Only trace the critical path within the dag_id specified",
)
@click.option(
    "--only-task-instances",
    is_flag=True,
    help="Only extract the task instances to calculate critical path. Uses dependencies already in the duckdb dependencies table.",
)
@click.option(
    "--skip-extract",
    is_flag=True,
    help="Skip all extracts and just calculate the critical path",
)
@click.pass_context
def trace(
    ctx: click.Context,
    username: str,
    password: str,
    baseurl: str,
    end_task_id: str,
    end_dag_id: str,
    dag_run_id: str,
    dag_ids_to_trace: str,
    dag_ids_to_trace_regex: str,
    output: str,
    delete_db: bool,
    stay_within_dag: bool,
    only_task_instances: bool,
    skip_extract: bool,
) -> None:
    """Extract all data and trace a critical path."""
    auth = HTTPBasicAuth(
        username or input("Enter Airflow username: "),
        password or getpass.getpass("Enter Airflow password: "),
    )

    if delete_db and os.path.exists(output):
        if only_task_instances:
            logging.info(
                "Skipping DuckDB deletion since --only-task-instances was provided"
            )
        elif skip_extract:
            logging.info("Skipping DuckDB deletion since --skip-extract was provided")
        else:
            os.remove(output)
            logging.info(f"Deleted existing DuckDB file: {output}")

    # Construct the dag_ids_to_trace_list
    if stay_within_dag:
        logging.info(
            f"Only tracing within dag {end_dag_id} since --stay-within-dag was specified."
        )
        dag_ids_to_trace_list = [end_dag_id]
    elif dag_ids_to_trace:
        dag_ids_to_trace_list = [
            dag_id.strip() for dag_id in dag_ids_to_trace.split(",")
        ]
        if end_dag_id and end_dag_id not in dag_ids_to_trace_list:
            logging.info(
                f"The end dag '{end_dag_id}' is missing from the --dag-ids-to-trace list. Adding it."
            )
            dag_ids_to_trace_list.append(end_dag_id)
    elif dag_ids_to_trace_regex:
        logging.info(f"Fetching all dag_ids and filtering by regexes: {dag_ids_to_trace_regex}")
        all_dag_ids = get_all_dag_ids(baseurl, auth)
        dag_ids_to_trace_list = []
        regexes = [regex.strip() for regex in dag_ids_to_trace_regex.split(",")]
        for dag_id in all_dag_ids:
            if any(re.search(regex, dag_id) for regex in regexes):
                dag_ids_to_trace_list.append(dag_id)
        if end_dag_id and end_dag_id not in dag_ids_to_trace_list:
            logging.info(f"The end dag '{end_dag_id}' is missing from the regex-filtered list. Adding it.")
            dag_ids_to_trace_list.append(end_dag_id)
    else:
        logging.info("Fetching all dag_ids.")
        dag_ids_to_trace_list = get_all_dag_ids(baseurl, auth)

    if not dag_ids_to_trace_list:
        raise ValueError("`dag_ids_to_trace_list` cannot be empty")

    if only_task_instances:
        logging.info(
            "Skipping dependency extraction since --only-task-instances was provided"
        )
    elif skip_extract:
        logging.info("Skipping dependency extraction since --skip-extract was provided")
    else:
        etl_dependencies(baseurl, dag_ids_to_trace_list, dag_run_id, auth, output)

    if skip_extract:
        logging.info(
            "Skipping task instance extraction since --skip-extract was provided"
        )
    else:
        etl_task_instances(
            baseurl,
            dag_ids_to_trace_list,
            dag_run_id,
            auth,
            output,
            ctx.obj["page_length"],
        )
        logging.info(
            f"Finished extracting dependencies and task instances for DAG {end_dag_id} DAG Run: {dag_run_id}"
        )
    
    if not (end_dag_id and end_task_id):
        end_dag_id, end_task_id = find_final_task(duckdb_location=output, dag_run_id=dag_run_id)
        logging.info(f"No end_dag_id or end_task_id specified. Using the final task in the dag run: {end_dag_id}, {end_task_id}")

    critical_path = calculate_critical_path(
        end_task_id=end_task_id,
        end_dag_id=end_dag_id,
        dag_run_id=dag_run_id,
        duckdb_location=output,
    )

    [click.echo(o) for o in critical_path]


if __name__ == "__main__":
    cli()

    # cd ~/src/flightpath/tests/airflow_example; astro dev start; cd -

    # poetry run flightpath --verbose trace -u admin -p admin --baseurl http://localhost:8080 --end-task-id end --end-dag-id diamond2 --dag-run-id scheduled__2024-11-16T19:30:00+00:00 --output ~/Downloads/flightpath.db --delete-db
