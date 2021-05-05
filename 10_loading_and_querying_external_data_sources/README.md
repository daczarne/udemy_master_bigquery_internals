# External data sources

Avro files are the preferred for loading data into BigQuery. They can be read in parallel, even when compressed in data blocks. Files can be uploaded into buckets and then loaded into tables choosing the Google Cloud Storage source.

External data has one pseudo-column of metadata called `_FILE_NAME`. This column contains the fully qualified path to the file the row belongs to. Remember that alias is mandatory when querying pseudo-columns. This is only available when the data source is another Google product/service.

Limitations of external data sources:

- BigQuery can not guarantee the data consistency
- query performance may not be as high as with native tables
- cost estimation can not be provided before the query is run
- export jobs are not allowed
- can not use wild cards
- query results can not be cached
- not all regions are supported
