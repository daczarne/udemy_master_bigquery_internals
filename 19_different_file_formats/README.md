# Different file formats

## Text (csv and tsc)

- **Behavior:** each line is a data point and lines are terminated with a newline character (\n)
- Good write performance
- Slow read performance
- Do not support block compression
- Files are splittable
- Limited schema evolution

## Sequence files

- **Behavior:** each data point is stored as a key-value pair in binary format
- Good write performance
- Good read performance
- Support block compression
- Files are splittable
- Limited schema evolution

## Avro files

- **Behavior:** uses JSON for defining data types and serializes data in a compact binary format
- Good write performance
- Good read performance
- Support block compression
- Files are splittable
- Support full schema evolution

## RC files (Row-Columnar files)

- **Behavior:** data is stored in key-value pairs. RC files are columnar.
- Slow write performance
- Fast read performance
- Support block compression
- Files are splittable
- No schema evolution

## ORC files (Optimized Row-Columnar files)

They are similar in almost every aspect to RC files, but support better compression and easier to handle splits.

- **Behavior:** data is stored in key-value pairs. ORC files are columnar.
- Slow write performance
- Fast read performance
- Support block compression
- Files are splittable
- No schema evolution

## Parquet files

- **Behavior:** stores nested data structures in a flat columnar format
- Slow write performance
- Fast read performance
- Support block compression
- Files are splittable
- Limited schema evolution
