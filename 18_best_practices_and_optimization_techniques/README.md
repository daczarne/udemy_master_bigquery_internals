# Best practices and optimization techniques

## Reduce query costs

- Reduce the bytes read. Avoid `SELECT *`
- `LIMIT` does not reduce data scans
- Use table partitioning and clustering
- De-normalize data and take advantage of nested and repeated columns
- Create materialized views
- Cache query results
- Avoid external data sources as much as possible
- Reduce shuffling size: reduce data before `JOIN`

## Reduce CPU time

- Write transformed data into another table and perform aggregations on the new table
- Avoid JavaScript UDFs. Use [Native UDFs](https://cloud.google.com/bigquery/docs/reference/standard-sql/user-defined-functions#sql-udf-structure) instead
- Use [approximate aggregation](https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions) function when possible
- Avoid `ORDER BY` clause when possible
- Push regexp and complex mathematical functions to the end of queries (thus performing them on reduced data sets)
- Order `JOIN` tables form largest to smallest when possible. This enables table broadcasting

## Query outputs

- `LIMIT` clause reduces the amount of data being returned.

## BigQuery best practices

- Avoid self joins and use window functions instead
- Avoid cross joins. Pre-aggregating data or using window functions generally solves this requirement
- Re-partition the data to avoid data-skew problems
- Avoid DMLs for single row modifications. Batch inserts and updates
