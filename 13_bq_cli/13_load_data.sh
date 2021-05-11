# * Load data into table. If the table does not exist, it will be created.

bq load [<project_name>:]<dataset_name>.<table_name> <path_to_data_file> --schema <path_to_schema_file.json>
