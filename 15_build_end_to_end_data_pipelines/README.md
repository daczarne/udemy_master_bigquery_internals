# Build end-to-end data pipelines

The goal of this section is to build a data pipeline to ingest orders data from a fictitious online food-selling company. The data is stored in CSV batches.

Pipeline Architecture:

- **Input data:** we'll assume the data is already in Cloud Storage.
- **Ingestion layer:** because we are simulating the situation in which the data is already in cloud storage, we don't need an ingestion layer.
- **Processing layer:** data is not clean so we need a processing layer for data transformations. For this layer we'll use Cloud Dataflow. Transformations will be written in Apache Beam (sent via a Python script to the GCP servers).
- **Storage layer:** because we are using structured data, we'll storage it in BigQuery. This will allow data analysts to run SQL queries on it.
- **Scheduler**: since the pipeline needs to be run daily, we'll use Cloud Composer to schedule the jobs. This is a managed workflow orchestration service built on Apache Airflow.
