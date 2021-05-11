# BigQuery Command Line

One way of running CL commands is to activate the BQ shell. To do so, open it, and run

``` zsh
bq show
```

to activate it. After that, you can run any command-line command there. But a better way is to use the [BigQuery SDK](https://cloud.google.com/sdk/docs/install).

## Commands

BQ commands have two types of flags: **global flags** (can be used with any command), and **command-specific flags** (can only be used with a specific command). Global flags should always come before command specific flags. Every BQ command follows the following pattern:

``` zsh
bq --global_flag = value command_name --command_flag = value <project_name>:<dataset_name>.<table_name>
```

Commands can be broken up into different lines by using a backslash `\`.

The `show` command displays the information about an object. So, for example, if we run

``` zsh
bq show
```

it will display the list of projects that can be accessed with the logged in account. If you are not logged in, it'll give you instructions on how to log in. To see information about a specific dataset, run:

``` zsh
bq show --dataset <project_name>:<dataset_name>
```

To see the table schema, we use the `schema` flag:

``` zsh
bq show --schema <project_name>:<dataset_name>.<table_name>
```

If a certain project or data set ID has been provided with the credentials, we can omit them from the command.

We use the `ls` command to list entities inside a collection. An entity can be anything (a project, a dataset, etc).

``` zsh
bq ls
```

Use the `help` command to get detailed information about the BQ command-line. If a command name is included, then help information for that specific command will be shown.

``` zsh
bq help [<command_name>]
```

Use the `cancel` command to cancel a BQ job. A job ID is mandatory with this command.

``` zsh
bq cancel <job_id>
```

To avoid having to use the `bq` keyword with every command, start an interactive shell first with the `shell` command.

``` zsh
bq shell
```

When done, you can exit it by simply running the `exit` command.

## Global flags

Global flags include

- `--location` will run the command at the location value
- `--format` specifies the format of the output: `pretty`, `sparse`, `prettyjson`, `json`, `csv`
- `--job_id` used to specify the job ID. Applies only to commands that generate jobs

A complete list of global flags can be found [here](https://cloud.google.com/bigquery/docs/reference/bq-cli-reference#bq_global_flags).

## Query commands

To run a SQL query via command line use the `query` command. To use Standard SQL, set the `--use_legacy_sql` flag to `false`, and then provide a valid SQL statement. In Cloud shell, the query statement needs to be written in single quotes, `'`. In the local SDK, the quotes can either be removed entirely, or replaced with double-quotes `"`.

``` zsh
bq query --use_standard_sql=false <query_statement>
```

Flags:

- `--append_table` will write query results to the supplied `--destination_table`
- `--replace` will replace data in `--destination_table` with query results. Its default value is `false`
- `--destination_schema` specify the schema for the `--destination_table`. Only needed if the destination table does not yet exist
- `--time_partitioning_field` will partition the table based on the time column provided
- use `--time_partitioning_type` to partition table based on ingestion time. Values can be `DAY`, `HOUR`, `MONTH`, or `YEAR`
- use `--time_partitioning_expiration` to set the expiration (in seconds) for the table or view partitioning. A negative value indicates no expiration.
- `--clustering_fields` is a list of up to 4 comma separated column names on which to cluster the destination table
- use `--destination_kms_key` to provide the resource ID of a customer generated encryption key
- keep `--batch` equal to `true` if you want the query to be run in batch mode
- `--maximum_bytes_billed` will set the maximum number of bytes that are allowed for query statements. If the query exceeds the limit, it fails without generating cost.
- use the `--label` flag to apply flags to a query in the form of key-value pairs. To pass multiple pairs, repeat the flag
- `--dry-run` is a boolean flag that acts as a validator for the command. When set to `true`, the query is validated but not run. It is `true` by default
- `--max-rows` takes an integer specifying the number of rows to return in the query results. Default is 100.
- if `--require_cache` is set to `true` then the query will only be run if it can be retrieved from the cache. By default it's `false`.
- set `--use_cache` to `false` if you don't want the query to cache results.
- use the `--schedule` flag to specify a Cron compatible scheduling value.
- `--display_name` allows us to name the schedule
- with `--target_dataset` we can supply a different dataset for where to store query results. This can not be used in conjunction with the `--destination_table` flag.
- `--allow_large_results` enables lard destination table sizes for legacy SQL queries
- `--flatten_results` boolean that when set to `true` will flatten nested and repeated fields
- `--udf_resource` specifies the Cloud Storage URI or the path to a local UDF code file. Repeat for multiple UDFs.

Boolean flags can be simplified by appending the `no` keyword in front of the flag. So `--nouse_cache` is the same as `--use_cache=false`.

## Dataset creation

Entities can be created with the `mk` command with the `--dataset` flag (or its shortcut `-d`). If both flag and its shortcut are omitted, then the `mk` command defaults to creating a dataset

``` zsh
bq mk --dataset
```

Additional flags can be use to set the dataset options.

## Table creation

To create tables use the `mk` command with the `--table` flag or the `-t` shortcut.

``` zsh
bq mk --table <project_name>:<dataset_name>.<table_name>
```

Additional flags can be use to set the table options. For example:

- use the `--expiration` flag to set the table expiration in seconds
- use the `--description` flag to set the table description
- use the `--label` flag to set a label in the form of `key:value` pairs. You can set as many labels as you want by repeating the flag
- set `--require_partition_filter=true` to enforce the usage of table partitions
- set `--time_partitioning_type` to `DAY` to make the table an ingestion time partitioned table (on ingestion day). It can also be `HOUR`. The default is `DAY`
- use the `--time_partitioning_expiration` to set an expiration number of seconds for the partitions
- use the `--time_partitioning_field <column_name>` flag to set the partition based on `<column_name>`
- use the `--integer_partitioning <column_name>,<start_value>,<end_value>,<interval>` to set an integer partitioning based on `<column_name>` that starts at `<start_value>`, ends at `<end_value>`, and uses `<interval>` steps
- use the `--clustering_fields` flag to set up table clustering
- use the `--schema` to supply the table schema. This can be done in line, or by setting the flag value to the path to a JSON file containing the table schema. In-line schemas must be supplied using `key:value` pairs and they don't support specifying column descriptions, or mode. All columns are set to `NULLABLE` mode. JSON schema files must be in a locally accessible location (cloud resources are not allowed).

## Loading data into tables

To load data into tables we use the `load` command. We need to supply the table name and its schema too. If the table does not exist, it will be created with the supplied schema.

``` zsh
bq load [<project_name>:]<dataset_name>.<table_name> <path_to_data_file> --schema <path_to_schema_file.json>
```

We can also use the `--auto-detect` flag instead of supplying a schema definition. All options from the UI are available in the CLI in the form of flags.
