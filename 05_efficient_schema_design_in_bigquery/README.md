# Efficient schema design

BigQuery performs best when data is de-normalized. To do so, it uses nested and repeated column schemas. This causes redundancy in storage, but speeds up querying. De-normalization can cause queries to be slower when grouping by columns that maintain a one-to-many relationship. To avoid this, BigQuery supports nested columns. Nested columns use `STRUCT` data type, and repeated columns use `ARRAY` data type.

Tables with nested data can be created from object files (like JSON, Avro, etc.). When uploading, to instruct BigQuery that a field is of `STRUCT` type, we select the `RECORD` type and the `REPEATED` mode. Once we select the `RECORD` type, a `+` sign will appear next to the filed name. Upon clicking it, we'll be able to add nested fields.

To un-nest the fields when querying, we use the `CROSS JOIN` query statement.
