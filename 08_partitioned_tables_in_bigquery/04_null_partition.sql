/* Rows with missing values for the partitioning column will be included in the __NULL__ partition. */

SELECT *
FROM [dataset1.demo_part_date$__NULL__]
