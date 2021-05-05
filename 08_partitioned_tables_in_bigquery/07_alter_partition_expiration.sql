/* We can alter the tables partition expiration time/date */

ALTER TABLE `bigquery-demo-285417.dataset1.demo_part_ingestion`
SET OPTIONS (partition_expiration_days = 10)
