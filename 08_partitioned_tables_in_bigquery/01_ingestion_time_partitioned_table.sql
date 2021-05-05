/* When selecting partition pseudo-columns we must always use an alias. */
SELECT
  _PARTITIONTIME AS partition_time
  , _PARTITIONDATE AS partition_date
  , name
FROM `bigquery-demo-285417.dataset1.demo_part_ingestion`
WHERE _PARTITIONDATE = DATE('2020-08-22')