# Partitioned tables

A partitioned table is a table that is divided into segments (called partitions) based on some criteria. This makes is easier to manage and query data. When partitioning, the files containing the data are spread based on the partitioning criteria. This optimizes queries both in execution time and cost since only the requested partitions will be used (hence the total number of bytes processed will decrease). Partition also speeds up queries in two ways. First, less data needs to be scanned. But also, when conducting aggregations based on the partitioning column, each batch can be processed in parallel.

Independent partitions can be managed independently. They can even live on different disk sub-systems. This means that less frequently accessed data can be stored in slower disks, and more frequently accessed data can be stored on faster disks.

In BigQuery, tables can be partitioned by one of:

- Ingestion time (can be either hourly partitioned or daily partitioned)
- Date or timestamp columns
- Integer columns

Tables partitioned by ingestion time will have a pseudo-column called `_PARTITIONDATE` if hourly partitioning was used, or two pseudo-columns `_PARTITIONTIME` and `_PARTITIONDATE` if daily partitioning was used. `_PARTITIONTIME` pseudo-columns contain a time stamp representation of the time in which the partition was ingested. `_PARTITIONDATE` contains the date in which the partition was ingested. Both pseudo-column names are reserved language keywords.

We can read meta data form the partitions by accessing the `__PARTITIONS_SUMMARY__` read-only tables. This needs to be done in legacy SQL since standard SQL does not yet support the `$__<table_name>__` decorator. This table contains all the information regarding the partitions in a given data set. Keep in mind that all time values use UTC timezone.
