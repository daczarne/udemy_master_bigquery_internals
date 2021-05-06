/* Call the refresh system process to update MVs manually. */

CALL BQ.REFRESH_MATERIALIZED_VIEW('bigquery-demo-285417.dataset1.names_mv')
