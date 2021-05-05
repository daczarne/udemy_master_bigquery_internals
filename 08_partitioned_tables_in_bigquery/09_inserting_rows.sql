/* If the table was partitioned by ingestion date, remember to specify the partition to which the new row needs to be added. */

INSERT
INTO `bigquery-demo-285417.dataset1.demo_part_ingestion` (_PARTITIONTIME, name, gender, count)
VALUES (TIMESTAMP("2020-09-17"), "Kiu", "F", 100)
