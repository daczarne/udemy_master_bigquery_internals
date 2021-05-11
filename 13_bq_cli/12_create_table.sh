#* Create a table

bq mk
--table
--expiration 3000
--description "Table description goes here"
--label dummy_key1:value1
--label dummy_key2:value2
--require_partition_filter
--time_partitioning_type DAY
--time_partitioning_expiration 4000
--clustering_fields name
--schema "<path_to_json_file> [<project_name>:]<dataset_name>.<table_name>"
