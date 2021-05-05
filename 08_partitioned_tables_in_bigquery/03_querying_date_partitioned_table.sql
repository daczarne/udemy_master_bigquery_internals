/* The partition can be used in the WHERE clause. This can be set to be a mandatory requirement. */

SELECT *
FROM `bigquery-demo-285417.dataset1.demo_part_date`
WHERE mydate = DATE("2020-01-19")
