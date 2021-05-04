/* Deleted data can be recovered within 7 days from deletion. */

-- DELETE FROM `bigquery-demo-285417.dataset1.names2` WHERE 1 = 1

SELECT *
FROM `bigquery-demo-285417.dataset1.names2`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
