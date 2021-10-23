from contextlib import ExitStack
from unittest.mock import patch

from extract import get_bigquery_client


def test_bigquery_service_should_create_bigquery_client_with_defined_arguments():
    with ExitStack() as stack:
        mock_client = stack.enter_context(patch("extract.bigquery.Client"))
        mock_service_account = stack.enter_context(
            patch("extract.service_account.Credentials.from_service_account_info")
        )

        bq_credential_secret = {
            "type": "service_account",
            "project_id": "project-something",
        }
        bq_project_id = "bq_project_id"
        get_bigquery_client(bq_credential_secret, bq_project_id)

        mock_service_account.assert_called_once_with(bq_credential_secret)
        mock_client.assert_called_once_with(credentials=mock_service_account.return_value, project=bq_project_id)


def test_bigquery_service_should_get_bigquery_client():
    with ExitStack() as stack:
        mock_client = stack.enter_context(patch("extract.bigquery.Client"))
        mock_service_account = stack.enter_context(
            patch("extract.service_account.Credentials.from_service_account_info")
        )
        expected = mock_client.return_value = "bigquery_client_object"

        bq_credential_secret = {
            "type": "service_account",
            "project_id": "project-something",
        }
        bq_project_id = "bq_project_id"
        bigquery_client = get_bigquery_client(bq_credential_secret, bq_project_id)

        assert bigquery_client == expected
