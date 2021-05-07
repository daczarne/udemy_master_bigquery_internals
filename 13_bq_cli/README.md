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
