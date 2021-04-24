# Hierarchy of GCP resources

``` txt
Organization
  |_ Folders
    |_ Projects
        |_ Resources
```

A resource is any GCP service the organization is using for that project. In case of Google BigQuery, resource hierarchy is as follows

``` txt
Organization
  |_ Folders
    |_ Projects
        |_ Data Sets
            |_ Tables
            |_ Views
```

Every time a resource is used (for example, running a query on BigQuery), a **job** is run.

## Data Sets

Data sets names can contain up to 1024 characters including upper and lower letters, numbers, and underscores. They are case sensitive. When creating a data set, we must also specify a location. By default, that location will be US. There are two types of locations, region and multi-region. A region is a specific place for the data center. A multi-region contains multiple regions. When using multi-regions, Google will make a copy of the data in each region to reduce latency when consuming the data. All external resources must be in the same region (or multi-region) as the data set that uses it. The location and name of a data set can only be set at creation time.

There can be as many data sets in a project as you need, and as many tables inside each data set as you need. But, as the number increases, UI performance will be impacted. The UI will only display the first 50,000 tables in a data set. Additionally, there can only be up to 2,500 views in a data set's control list.

## Tables

In BigQuery we do not need to first create the table and then insert the data into it. We can do both steps in one.

When defining a table schema manually, each column must:

1. have a name containing only letters and underscores
2. have a maximum of 128 characters
3. can not use _TABLE_, _FILE_, or *_PARTITION*
4. two or more columns can not have the same name
5. column names are case insensitive

Column modes include:

- **NULLABLE** which allows columns to be null (it's the default mode)
- **REQUIRED** null values are not allowed
- **REPEATED** column values must fall within an array of specified values
