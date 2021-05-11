#* Create a dataset

bq mk \
--default_table_expiration 4000 \
--default_partition_expiration 5000 \
--description "Dataset description goes here" \
[<project_name>:]<dataset_name>
