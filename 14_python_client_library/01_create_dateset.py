from google.cloud import bigquery

#* Set service account key
SERVICE_ACCOUNT_JSON = r'<path_to_key.json>'

#* Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

#* Set dataset_id to the ID of the dataset to create.
dataset_id = "<project_name>.<dataset_name>"

#* Construct a full Dataset object to send to the API using the Dataset class.
dataset = bigquery.Dataset(dataset_id)

#* Specify the geographic location where the dataset should reside. Other dataset attributes can be found in the documentation: https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.dataset.Dataset.html
dataset.location = "US"
dataset.description = "dataset description"

#* Send the dataset to the API for creation, with an explicit timeout. Raises google.api_core.exceptions.Conflict if the Dataset already exists within the project.
dataset_ref = client.create_dataset(dataset, timeout = 30)  # Make an API request.

print("Created dataset {}.{}".format(client.project, dataset_ref.dataset_id))
