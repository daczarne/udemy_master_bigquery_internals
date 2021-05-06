/* Create a materialized view */

CREATE MATERIALIZED VIEW `bigquery-demo-285417.dataset1.names_mv`
AS
SELECT 
  name
  , SUM(count) AS total_count
FROM `bigquery-demo-285417.dataset1.names`
GROUP BY name
