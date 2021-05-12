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

## Table creation

To create a table we use the `LoadJobConfig` class. A complete list of attributes of the class can be found [here](https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.LoadJobConfig.html). The `schema` attribute can be set with a python `list` or a JSON file.

If the data is in disk we read it as we would normally do in Python. If its in a cloud storage system, then we do the same, but passing the url as the path argument to the `open` function.

Once a `job` object is created, we can call the `result` method for the table to be created. But if we want to see the uploaded data we need to call the `get_table` method of the `client` object.

As with the create dataset script, we just need to run it in terminal once we are finished:

``` python
python3 <path_to_script.py>
```

## Query tables

To run a query just create the query statement as a character string, and pass it as the argument of a call to the `query` method of the `Client` instance that you've defined.

Since the query statement can be any valid statement (DDL or DML), we can use this same approach to create tables, views, materialized views, etc.

The downside with this method is that since the `query` string is just a string for the Python interpreter, you will not be warned of any errors.
