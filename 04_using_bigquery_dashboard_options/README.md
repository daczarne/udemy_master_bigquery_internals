# Using BigQuery

When running a query GBQ will display the amount of data that is been processed. If we run the same query we will not be charged since GBQ caches query results.

On the query setting dropdown menu we can change how the query is executed. **Query engine** determines how the query is run: 

- BigQuery engine: for batch processing.

- Cloud Dataflow engine: for stream processing.

Next we can select how query results should be saved. By default, GBQ saves all query results to a temp table. These temp tables are not available to users and thus, can not be queried or shared. They do not generate costs. They are the tables responsible for caching the query results. They last for 24 hrs.

When writing to permanent tables we need to also select the disposition (*write if empty*, *append to table*, or *overwrite table*). The tables been queried must be in the same location as the destination data set. The "Allow large results" checkbox enables results larger than 10GB (the max default limit).

**Job priority** determines how the job is executed. *Interactive* jobs are run immediately. *Batch* jobs start as soon as resources are available in the shared resource pool.

# Caching

In order for GBQ to cache results, the query statement should be exactly the same. They are also not cached if their is a destination table specified to store the results (CREATE, INSERT, etc). They will be re-run if the tables or views used in the query have changed. Query results can never be cached for tables with streaming ingestion. They also cannot be cached if the query uses non-deterministic functions (like NOW(), CURRENT_USER(), CURRENT_DATE(), etc). Queries will not be cached if they use external results (like BigTable or CloudStorage). Lastly, the result set must be smaller than 10GBs to be cached.
