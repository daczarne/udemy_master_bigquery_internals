from google.cloud import bigquery

SERVICE_ACCOUNT_JSON = r"<path_to_json_key"

#* Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

#* Build the query statement
query = """
	query statement goes here
"""

#* Make an API request using the query method from the Client class
query_results = client.query(query)

#* Print results
print(query_results)
print("Script run")
for row in query_results:
	print(str(row[0]) + "," + str(row[1]) + "," + str(row[2]))
