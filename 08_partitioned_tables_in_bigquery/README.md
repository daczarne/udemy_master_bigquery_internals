# Partitioned tables

A partitioned table is a table that is divided into segments (called partitions) based on some criteria. This makes is easier to manage and query data. When partitioning, the files containing the data are spread based on the partitioning criteria. This optimizes queries both in execution time and cost since only the requested partitions will be used (hence the total number of bytes processed will decrease). Partition also speeds up queries in two ways. First, less data needs to be scanned. But also, when conducting aggregations based on the partitioning column, each batch can be processed in parallel.

Independent partitions can be managed independently. They can even live on different disk sub-systems. This means that less frequently accessed data can be stored in slower disks, and more frequently accessed data can be stored on faster disks.

In BigQuery, tables can be partitioned by one of:

- Ingestion time (can be either hourly partitioned or daily partitioned)
- Date or timestamp columns
- Integer columns

## Ingestion time partitioning

Tables partitioned by ingestion time will have a pseudo-column called `_PARTITIONDATE` if hourly partitioning was used, or two pseudo-columns `_PARTITIONTIME` and `_PARTITIONDATE` if daily partitioning was used. `_PARTITIONTIME` pseudo-columns contain a time stamp representation of the time in which the partition was ingested. `_PARTITIONDATE` contains the date in which the partition was ingested. Both pseudo-column names are reserved language keywords.

We can read meta data form the partitions by accessing the `__PARTITIONS_SUMMARY__` read-only tables. This needs to be done in legacy SQL since standard SQL does not yet support the `[<dataset_name>.<table_name>$__PARTITIONS_SUMMARY__]` decorator. This table contains all the information regarding the partitions in a given table. Keep in mind that all time values use UTC timezone.

## Date partitioned tables

Rules for partitioning by date column

- the partitioning column must be a scalar date or timestamp column with mode `NULLABLE` or `REQUIRED` (it can not be `REPEATED`)
- the partitioning column must be a top-level field (it can not be a leaf column from a `STRUCT`)

The `_PARTITIONTIME` pseudo-column will not be crated since the partitioning column is present in the data itself. Rows with no value for the partitioning column will be included in the `__NULL__` partition. Rows with date values outside the allowed range of dates will be included in the `__UNPARTITIONED__` partition. This partition also holds the un-partitioned data from real-time buffer streams.

## Integer partitioned tables

Rules for partitioning by integer column

- the partitioning column must be of integer type
- the partitioning column must not have a `REPEATED` mode
- the partitioning column must be a top-level filed
- an integer range can be set for the partition values (start value is inclusive, but end value is exclusive)

Rows with missing data for the partitioning column will be stored in the `__NULL__` partition, and rows with partitioning values outside of the partitioning range will be stored in the `__UNPARTITIONED__` partition.

## Limitations of partitions

- the maximum number of partitions allowed is 4,000
- the maximum number of partitions modified by a single job is 4,000
- the maximum number of partitions modified per day is 5,000 for ingestion time partitioned tables, or 30,000 for date or integer partitioned tables

## DML statements on partitioned tables

Other than the ability to use the partitions, partitioned tables are not different that non-partitioned tables. In addition to all standard manipulations, you can also set a partition expiration date. You can do this with an `ALTER TABLE` statement. Different expiration times can not be set for different partitions. Table expiration takes precedence over partition expiration.

When deleting data, keep in mind that you can't delete the `__NULL__` nor the `__UNPARTITIONED__` partitions.

Insertion of new rows can be done just as with non-partitioned tables. Just keep in mind that if the table is ingestion partitioned, then we must supply the `_PARTITIONTIME` to which the new rows must be inserted.

## Best practices

- use partition filters (`WHERE` statement that uses the partitioning column)
- `AND` conditions don't remove partition elimination, but `OR` conditions do
- functions of partitions columns don't allow for partition elimination
- `WHERE` clauses that use sub-query expressions that use the same table don't allow for partition elimination
- when used for partition elimination, pseudo-columns must always be on the right-side of the comparison (as to avoid calculations on pseudo-columns). This means that we should prefer

``` sql
SELECT  *
FROM `bigquery-demo-285417.dataset1.demo_part_ingestion`
WHERE _PARTITIONTIME > TIMESTAMP_SUB(TIMESTAMP('2020-09-15'), INTERVAL 1 DAY)
```

over

``` sql
SELECT *
FROM `bigquery-demo-285417.dataset1.demo_part_ingestion`
WHERE TIMESTAMP_ADD(_PARTITIONTIME, INTERVAL 1 DAY) > '2020-09-15'
```

- don't compare partition columns to other columns in the table
- don't create too many partitions in a table
