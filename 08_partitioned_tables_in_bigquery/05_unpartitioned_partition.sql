/* Rows with values out side the date range will be included in the __UNPARTITIONED__ partition. */

SELECT *
FROM [dataset1.demo_part_date$__UNPARTITIONED__]
