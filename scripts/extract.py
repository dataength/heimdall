import json

from google.cloud import bigquery
from google.oauth2 import service_account


with open("conf.json", "r") as f:
    config = json.load(f)

bigquery_credential_secret = config["bigquery_credential_secret"]
client = bigquery.Client(
    credentials=service_account.Credentials.from_service_account_info(
        bigquery_credential_secret,
    ),
    project=config["project"],
)

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
