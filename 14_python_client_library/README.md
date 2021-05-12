# Python client library

We need to set up a service account key to access BigQuery via APIs. Head on to *IAM & Admin > Service Accounts > + CREATE SERVICE ACCOUNT*. Now provide a name for it and click *CREATE*. You can set up privileges in the authentication key (for example, project editor). Then click *CONTINUE*. If needed, grant users access to the service account, then click *DONE*.

The Google UI will display the list of service accounts. Go to *Actions* and *Create key*. Recommended key type is JSON. Click create and a JSON file will be downloaded onto your computer. This JSON file will be embedded on the project. **DO NOT SHARE THE KEY!!**

## Create dataset

The path to the key can be specified in the Python code or as an environment variable using the command line: `SET_SERVICE_ACCOUNT_JSON=<path_to_key>`.

Attributes for the `Dataset` class can be found [here](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.dataset.Dataset.html). The dataset itself can be created using the `create_dataset` method from the `Client` class. Documentation on the `Client` class can be found [here](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html).

Once the script is finished just run it from the terminal:

``` python
python3 <path_to_script.py>
```
