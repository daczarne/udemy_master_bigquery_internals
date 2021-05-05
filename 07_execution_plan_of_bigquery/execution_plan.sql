SELECT
  MAX(ROUND((max - 32) * 5 / 9, 1)) celsius
  , mo
FROM `bigquery-public-data.noaa_gsod.gsod195*`
WHERE max != 9999.9
GROUP BY mo
ORDER BY mo DESC


