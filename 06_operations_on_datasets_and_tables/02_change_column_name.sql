/* Since changing column names is not yet supported, we can do it with a DML statement. To do so, we use a SELECT statement to select all columns, provide the new alias, and over write the table. When running this query, we can add a DELETE + an INSERT statement, or go to query settings and change the destination to be the same table and select the write preference to be Overwrite table. While this method saves all the data, charges can be large if it involves a lot of data. */

SELECT 
  * EXCEPT(name)
  , name AS first_name
FROM `bigquery-demo-285417.dataset1.names2`
