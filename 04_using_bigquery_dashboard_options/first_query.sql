Select
  name
  , count
FROM `bigquery-public-data.tablename`
WHERE gender = 'M'
ORDER BY count DESC
LIMIT 10