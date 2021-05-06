# Materialized views

A Materialized View is a View that is stored on disk (i.e. it does have its own data). When queried these views don't refer there base tables. The data will be the same until a refresh is done. This can be automated.

Because MVs are in beta they can only be created in the same dataset as the tables it uses. They also inherit the expiration of the tables. MVs can only query data from one table, and they must be aggregations of said table. Only a few aggregations are already supported. `HAVING` clause is not yet supported.

When running queries, BigQuery will check if it (or any sub-query) can be found in an MV and use it if there is.

MVs can use partition and clustering. To use partitioning, the base table needs to be partitioned too, and the MV inherits it.

## Altering MVs

MVs can be alter with created, edit, and delete jobs. But, copy, import, or export jobs are not supported. Using the `INSERT` statement is not possible either. Neither is using the BigQuery Storage API.

If the base table for an MV is dropped, the MV will stop refreshing and any query that uses the MV will fail. The MV will have to be recreated, even if the base table is recreated using the exact same name.

## MV refreshing

The default refresh mechanism depends on the alterations done to the base table. When available, partitions will be used to update the MV. To update an MV manually, just call the `REFRESH_MATERIALIZED_VIEW` system process. The name of the MV needs to be supplied as a character string.

By default, MVs are automatically refreshed within 5 minutes of the changes to the base tables. This mechanism needs to be enabled at creation time or it can be altered afterwards. We can also set the refresh time in a creation or alter statement. The minimum is 1 minute, and the maximum is 7 days.

If the base table has changed at the time of querying the MV, the result of the query MV will still be up-to-date. BigQuery runs the following steps if the base table suffered an append process:

1. fetch all materialized data
2. read the table delta
3. adjust aggregations as per delta
4. return query results

If the base table suffered updates or deletions, then the materialized view might not even get scanned, and the query re-directed to the base table.
