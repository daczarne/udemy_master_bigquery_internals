/* As with changing the name, we can use the same strategy for changing the column type. Standard casting rules apply here. */
SELECT
  * EXCEPT(count)
  , CAST(count AS STRING) AS count
FROM `bigquery-demo-285417.dataset1.names2`
