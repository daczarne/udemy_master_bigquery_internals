from google.cloud import bigquery

SERVICE_ACCOUNT_JSON = "path_to_key.json"

#* Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)

# TODO(developer): Set dataset_id to the ID of the dataset to create.
dataset_id = "project_name.dataset_name"

#* Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

# TODO(developer): Specify the geographic location where the dataset should reside.
dataset.location = "US"
dataset.description = "my new dataset"

#* Send the dataset to the API for creation, with an explicit timeout. Raises google.api_core.exceptions.Conflict if the Dataset already exists within the project.
dataset_ref = client.create_dataset(dataset, timeout = 30)  # Make an API request.

print("Created dataset {}.{}".format(client.project, dataset_ref.dataset_id))
