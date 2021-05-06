/* Create a view that contains only the rows to which the user has access to. */

SELECT *
FROM `bigquery-demo-285417.dataset1.names_with_user`
WHERE email = SESSION_USER()
