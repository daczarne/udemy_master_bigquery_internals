/* We can alter how often the MV is refreshed. */

ALTER MATERIALIZED VIEW `bigquery-demo-285417.dataset1.names_demo_mv1`
OPTIONS (
  enable_refresh = true
  , refresh_interval_minutes = 60
)
