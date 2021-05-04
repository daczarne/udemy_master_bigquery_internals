/* Same can be done to delete columns. Be careful with data losses when deleting columns. */

SELECT * EXCEPT(count)
FROM `bigquery-demo-285417.dataset1.names2`
