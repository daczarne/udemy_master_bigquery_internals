# Build end-to-end data pipelines

The goal of this section is to build a data pipeline to ingest orders data from a fictitious online food-selling company. The data is stored in CSV batches.

Pipeline Architecture:

- **Input data:** we'll assume the data is already in Cloud Storage.
- **Ingestion layer:** because we are simulating the situation in which the data is already in cloud storage, we don't need an ingestion layer.
- **Processing layer:** data is not clean so we need a processing layer for data transformations. For this layer we'll use Cloud Dataflow. Transformations will be written in Apache Beam (sent via a Python script to the GCP servers).
- **Storage layer:** because we are using structured data, we'll storage it in BigQuery. This will allow data analysts to run SQL queries on it.
- **Scheduler**: since the pipeline needs to be run daily, we'll use Cloud Composer to schedule the jobs. This is a managed workflow orchestration service built on Apache Airflow.

## Running the pipeline

The pipeline can now be run on the local SDK or on Google Cloud Shell. To run it on cloud shell, go to the GCP console and open the cloud shell. First you need to install the Apache Beam package in the cloud shell. To do so, run:

``` zsh
pip install apache-beam[gcp]
```

Upload the code with the *Upload File* option on the cloud console. You can use the `ls` command to make sure that the file is there. Now you just have to run the code. Remember that this file takes an `--input` parameter set to the path to the data file in cloud storage. Additionally, a location for the temp files must be provided. Use the `--temp_location` arg to specify it (alternatively, you could supply this in the code).

``` zsh
python <file_name.py> --input <path_to_cloud_storage_data_file.csv> --temp_location <bucket_name>
```
