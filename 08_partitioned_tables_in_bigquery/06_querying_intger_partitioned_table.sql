/* We can use a BETWEEN clause when querying integer partitioned tables. */

SELECT *
FROM `bigquery-demo-285417.dataset1.demo_part_ingestion`
WHERE dept BETWEEN 30 AND 50
