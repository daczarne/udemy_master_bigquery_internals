#* Table schema can be relaxed during a load or query command. 

bq load \
--schema_update_option ALLOW_FIELD_RELAXATION \
<project_name>:<dataset_name>.<table_name> <path_to_data_file> <path_to_schema_file.json>
