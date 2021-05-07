# * When using multiple flags it's better to break down the code with \

bq query \
--use_legacy_sql=false \
--label <key:value> \
--label <key:value> \
--batch=false \
--maximum_bytes_billed=30000000 \
--require_cache=false \
--destination_table=<project_name>:<dataset_name>.<destination_table_name> \
--destination_schema <col_name:col_type>,<col_name:col_type>,<col_name>:<col_type> \
--time_partitioning_type=DAY \
--time_partitioning_expiration=90000 \
--clustering_fields=<col_name>
"SELECT * FROM `project.dataset.source_table`"
