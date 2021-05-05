/* Delete partitions in a partition table by specifying the value of the pseudo-column */

DELETE
FROM `bigquery-demo-285417.dataset1.demo_part_ingestion`
WHERE _PARTITIONTIME = TIMESTAMP("2020-09-17")
