# Views

Views are virtual tables populated with the result of a SQL query. They do not hold the data. Views are independent of the base tables schemas. They are read only. If the base tables are deleted, queries on Views will fail. Views are used to provide access to the data without exposing the data. Views don't have a storage cost (since they don't actually hold any data), but querying Views will generate cost.

Since in BigQuery access can only be restricted at the data set level, Views should be created in a different data set than that where the original data is (since the goal is to keep that data out of reach).

Views allow access to rows. This can be done by creating a new column with the information of the user that is allowed to see that row. To do so, we use the `SESSION_USER()` function, which returns the email address of the current user. You can see the user by running

``` sql
SELECT SESSION_USER()
```

The viewing user must be included in the original data. If multiple users need to have access to the same row, then the column that contains the users emails must be a repeated filed. To avoid overhead, you can create a new table with each user and the group to which it belongs, and then add the group that can access it in the table with the data.

## Limitations

- The data set and its tables have to be in the same location
- Data from Views can not be exported (since there is none to export)
- Standard and Legacy SQL can not be mixed when creating and querying views
- Can not reference query parameters in Views
- Can not use UDFs in the query that defines the View
- Wildcard table queries are not supported for Views
- Maximum number of nested View levels is 16 (nested view = a view created from another view)
- Maximum number of views in a dataset is 2,500
