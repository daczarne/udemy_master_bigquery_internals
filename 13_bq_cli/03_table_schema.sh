# * Check the schema of <table_name>. The output will be formatted in pretty JSON.

bq show --schema --format prettyjson <project_name>:<dataset_name>.<table_name>
