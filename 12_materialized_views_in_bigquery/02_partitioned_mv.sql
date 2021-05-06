/* Materialized views can use partitions too */

CREATE MATERIALIZED VIEW bigquery-demo-285417.dataset1.names_mvd
PARTITION BY date
AS
SELECT
  name
  , SUM(count) AS total_count
  , _PARTITIONDATE AS date
FROM bigquery-demo-285417.dataset1.demo_part_ingestion
WHERE _PARTITIONDATE = "2020-02-19"
GROUP BY 1, 3
