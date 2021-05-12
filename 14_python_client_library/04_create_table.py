from google.cloud import bigquery

SERVICE_ACCOUNT_JSON = r"<path_to_json_key"

#* Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

#* Build the query statement
query = """
	CREATE TABLE <dataset_name>.<table_name>
  (
    x INT64 OPTIONS(description = "An optional INTEGER field"),
    y STRUCT<
        a ARRAY<STRING> OPTIONS(description = "A repeated STRING field"),
        b BOOL
      >
  )
  OPTIONS (
    expiration_timestamp = TIMESTAMP "2023-01-01 00:00:00 UTC",
    description = "A table that expires on 2023",
    labels = [
      ("org_unit", "development")
    ]
  )
"""

#* Make an API request using the query method from the Client class
query_results = client.query(query)
