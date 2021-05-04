SELECT 
  storeLocation
  , products
FROM `bigquery-demo-285417.dataset1.kiopl`
CROSS JOIN UNNEST(products) AS a
WHERE a.productName = "Grinder"