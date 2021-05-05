# BigQuery execution plan

When running a query, the BigQuery engine breaks the declarative SQL statements into more granular sets of execution stages and designs an execution graph. This allows the engine to determine which stages can be run in parallel, which can not, and which depend on results of previous stages and need to be queued. The execution plan is dynamic and repartition stages can be introduced as the job is executed to improve performance. During shuffling, BigQuery stores intermediate results in memory to make reduce and aggregation stages faster.

After running a query, the *Execution details* tab will display the execution plan that was used. It also displays execution metrics

- *elapsed time* displays the time elapsed since the start of the execution
- *slot time consumed* is the aggregated time consumed by the different slots, where a slot is a unit of computation capacity
- *bytes shuffled* displays the total number of bytes shuffled between stages
- *bytes spilled to disk* displays the total number of bytes that were written to disk. This is only done if the data to be shuffled is to big and can not be done all in-memory.

Below the metrics we can see a detailed description of every task in every stage. Stages are shown in rows, and tasks in columns. Cells display the average and maximum time (absolute as a number and relative as percentage bar) that each task required. To the far right of the table we can see the number of input and output rows for each stage. Both average and maximum times are generally measured in milliseconds, and represent how much time the worker nodes spent on each task at each stage. If we expand the information for each stage we can see a break down of the tasks involved in that stage.

Successful stages are labeled with a green check mark, while failed stages with a red exclamation mark.
