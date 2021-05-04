SELECT 
  storeLocation
  , products
FROM `bigquery-demo-285417.dataset1.kiopl`,
UNNEST(products) AS a
WHERE a.productName = "Grinder"