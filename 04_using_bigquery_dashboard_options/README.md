## Using BigQuery

When running a query GBQ will display the amount of data that is been processed. If we run the same query we will not be charged since GBQ caches query results.

On the query setting dropdown menu we can change how the query is executed. **Query engine** determines how the query is run:

- BigQuery engine: for batch processing.

- Cloud Dataflow engine: for stream processing.

Next we can select how query results should be saved. By default, GBQ saves all query results to a temp table. These temp tables are not available to users and thus, can not be queried or shared. They do not generate costs. They are the tables responsible for caching the query results. They last for 24 hrs.

When writing to permanent tables we need to also select the disposition (*write if empty*, *append to table*, or *overwrite table*). The tables been queried must be in the same location as the destination data set. The "Allow large results" checkbox enables results larger than 10GB (the max default limit).

**Job priority** determines how the job is executed. *Interactive* jobs are run immediately. *Batch* jobs start as soon as resources are available in the shared resource pool.

## Caching

In order for GBQ to cache results, the query statement should be exactly the same. They are also not cached if their is a destination table specified to store the results (`CREATE`, `INSERT`, etc). They will be re-run if the tables or views used in the query have changed. Query results can never be cached for tables with streaming ingestion. They also cannot be cached if the query uses non-deterministic functions (like `NOW()`, `CURRENT_USER()`, `CURRENT_DATE()`, etc). Queries will not be cached if they use external results (like BigTable or CloudStorage). Lastly, the result set must be smaller than 10GBs to be cached.

## Wildcard tables

When tables have the same schema and similar names (for example, `table_1`, `table_2`, `table_3`, etc) we can use wildcard expressions to query them all at once.

``` sql
SELECT
  col_1
  , col_2
FROM `project_name.dataset_name.table_name_*`
```

This shortens statements by eliminating the need of multiple `UNION ALL` statements. We can also use the `_TABLE_SUFFIX` pseudo-column selector.

``` sql
SELECT
  col_1
  , col_2
FROM `project_name.dataset_name.table_name_*`
WHERE (_TABLE_SUFFIX = '1' OR _TABLE_SUFFIX = '2' OR _TABLE_SUFFIX = '3')
```

We can even use the `BETWEEN` operator and simplify this query

``` sql
SELECT
  col_1
  , col_2
FROM `project_name.dataset_name.table_name_*`
WHERE _TABLE_SUFFIX BETWEEN '1' AND '3'
```

Keep in mind that cost reduction does not apply if the filter is the result of a sub-query that uses the dataset itself.

**Limitations**

- Wildcard tables can only be use with data that is in native BigQuery storage

- Cached results are not supported for wildcard queries

- DML statements are not allowed

## Scheduled queries

Schedule queries must be written in standard SQL (DDL or DML). First we write the query, and the un set up a Cron Job to execute them. The Schedule Query feature uses the services of the DataTransfer service in GCP. If you are not sure whether the Data Transfer API is enabled, search for it in the lookup bar and you'll be redirected to its dashboard (where you can enable it).

To schedule a query you must complete the scheduling form by supplying a name, a repeat interval (if you select custom, you must supply a [Cron style specification](https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml#the_schedule_format)), a start and end times. The result destination options will not be displayed if you are using a statement that already specifies them. You can specify a service account to which run the query using its credentials. If no service account is provided, then user credentials must be supplied.

It is recommended to also define the backfill mechanism that the query will use. Go to the schedule queries tab, click on the query, click on the more button, and select the backfill option. Keep in mind that start date is inclusive, while end date is not.
