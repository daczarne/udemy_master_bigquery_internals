from google.cloud import bigquery

SERVICE_ACCOUNT_JSON = r"<path_to_json_key"

#* Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

#* Set table_id to the ID of the table to create.
table_id = "<project_name>.<dataset_name>.<table_name>"

job_config = bigquery.LoadJobConfig(
	schema = [
		bigquery.SchemaField("name", "STRING"),
		bigquery.SchemaField("gender", "STRING"),
		bigquery.SchemaField("count", "INTEGER")
	],
	source_format = bigquery.SourceFormat.CSV,
	skip_leading_rows = 1,
	autodetect = True
)

file_path = r'<path_to_data_file>'

source_file = open(file_path, "rb")

job = client.load_table_from_file(source_file, table_id, job_config = job_config)

#* Waits for the job to complete.
job.result()

#* Make an API request.
table = client.get_table(table_id)

print("Loaded {} rows in {}".format(table.num_rows, table_id))
