#* Copy a partition from <source_table> to <destination_table>. If the destination table is not partitioned, data will be appended to the file(s). If it is partitioned, then a new partition will be added. To copy multiple partitions provide a comma separated list of partitions from the source table (dataset and table name need to be provided for every partition).

bq cp -a <source_dataset_name>.<source_table_name>$<partition> <destination_dataset_name>.<destination_table_name>
