import json
from typing import Dict

from google.cloud import bigquery
from google.oauth2 import service_account


def get_bigquery_client(bq_credential_secret: Dict[str, str], bq_project_id: str):
    return bigquery.Client(
        credentials=service_account.Credentials.from_service_account_info(bq_credential_secret),
        project=bq_project_id,
    )


if __name__ == "__main__":
    with open("conf.json", "r") as f:
        config = json.load(f)

    bigquery_credential_secret = config["bigquery_credential_secret"]
    bq_project_id = config["project"]
    client = get_bigquery_client(bigquery_credential_secret, bq_project_id)

    tables = client.list_tables(config["dataset"])
    for each in tables:
        print(each.table_id)

    query = f"""
        SELECT * FROM `{config["dataset"]}.INFORMATION_SCHEMA.COLUMNS`
    """
    query_job = client.query(query)
    rows = query_job.result()
    for each in rows:
        # columns:
        # table_catalog, table_schema, table_name, column_name, ordinal_position, is_nullable,
        # data_type, is_generated, generation_expression, is_stored, is_hidden, is_updatable,
        # is_system_defined, is_partitioning_column, clustering_ordinal_position
        print(each.values())
