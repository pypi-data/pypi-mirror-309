# spark-jdbc-ingestor
A library to handle JDBC ingestion from an SQL database in a simple and efficient way.

# Installing

## From a repository:
```
pip install git+https://github.com/efranceschi/spark-jdbc-ingestor.git
```

## From Pypi:
```
%pip install spark_jdbc_ingestor
```

# Get started

## Importing class
First, import the `JdbcIngestor` class and initialize an instance, passing an existing spark session, as well as the JDBC URL, username, password, and driver:
```
from spark_jdbc_ingestor import JdbcIngestor
jdbcIngestor = JdbcIngestor(spark=spark, url=jdbcUrl, user=user, password=password, driver=driver)
```

## Enabling logging (optional)
When investigating certain situations it is a good idea to enable logging to better understand what is happening:
```
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s[%(thread)d] - %(levelname)s - %(message)s')
```

# Ingesting Data

## Simple ingestion
The simplest way to do an ingestion is by specifying the source table and the target table:
```
df = (
    jdbcIngestor.from_table("source_table")
    .load()
    .overwrite("destination_table")
)
```

# Using a column to partition the data
You can configure execution parallelism, causing data to be partitioned in a way that distributes the processing load among workers.
Just choose a numeric, date, or timestamp column, as well as the number of partitions:
```
df = (
    jdbcIngestor.from_table("source_table")
    .load(partition_column="mycolumn", num_partitions=16)
    .overwrite("destination_table")
)
```

# Writing the data
You can choose to overwrite:
```
df = (
    jdbcIngestor.from_table("source_table")
    .load()
    .overwrite("destination_table")
)
```

or append the data in the destination table:
```
df = (
    jdbcIngestor.from_table("source_table")
    .load()
    .append("destination_table")
)
```

# Use a query instead of the table name
You can choose to use a query instead of a table. Just make sure you use the correct syntax, as shown in the following example:
```
df = (
    jdbcIngestor.from_query("(select * from source_table) as my_table")
    .load()
    .overwrite("destination_table")
)
```

# Advanced Ingestion

## Partial ingestion using filters
It is possible to perform partial ingestions by pushing predicates down to the JDBC database. This approach is especially useful for performing incremental ingestions, for example, based on dates or sequence identifiers.

The example below demonstrates the ingestion of yesterday's data:
```
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
start_date = yesterday.strftime('%Y-%m-%d 00:00:00')
end_date = yesterday.strftime('%Y-%m-%d 23:59:59')

df = (
    jdbcIngestor.from_table("source_table")
    .add_filter(
        f"last_changed between '{start_date}' and '{end_date}'"
    )
    .load()
    .overwrite("destination_table")
)
```

In this other example, only records with a sequence greater than 1000 are ingested:
```
last_id = 1000  # Assuming you can get this data from somewhere

df = (
    jdbcIngestor.from_table("source_table")
    .add_filter(
        f"id > {last_id}"
    )
    .load()
    .overwrite("destination_table")
)
```

You can also use the `get last_value()` utility function to easily get the largest value in the target database:
```
last_value = jdbcIngestor.get_last_value(
    table="destination_table",
    column="last_changed",
    default_value="1900-01-01 00:00:00",
)
```

Or you can combine everything at once:
```
df = (
    jdbcIngestor.from_table("source_table")
    .with_last_value(
        table="destination_table",
        column="last_changed",
        default_value="1900-01-01 00:00:00",
    )
    .load()
    .append("destination_table")
)
```

# How to choose the best column for partitioning?
If you don't know which column to choose to partition your data, use the `analyze()` function to obtain statistics and help you make your decision.
This function identifies all fields that qualify for partitioning and extracts the following information: min, max, avg, stddev, count, count distinct, as well as uniformity (count distinct / sample count) and completeness (count / sample count). The data is then ranked from the best column to the worst.

```
jdbcIngestor.from_table("source_table").analyze().show()
```

# Advanced ingestion using threading
Sometimes the size of the tables can be very large.
The example below uses threads to perform multiple ingestion operations, using filter push-downs in the source database to manually control the volume of data per day:
```
import logging
import concurrent.futures
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s[%(thread)d] - %(levelname)s - %(message)s')

def load_data_between(start_time, end_time):
    try:
        logger.info(f"> Loading data from {start_time} to {end_time}")
        return (
            jdbcIngestor.from_table("source_table")
            .add_filter(f"last_changed between '{start_time}' and '{end_time}'")
            .load(partition_column="id", num_partitions=8)
            .append("destination_table")
        )
    finally:
        logger.info(f"< Finished loading data from {start_time} to {end_time}")

futures = []
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    current_date, end_date = datetime(2020, 1, 1), datetime(2020, 12, 31)
    while current_date <= end_date:
        futures.append(
            executor.submit(
                load_data_between,
                current_date,
                current_date + timedelta(hours=23, minutes=59, seconds=59),
            )
        )
        current_date += timedelta(days=1)
    concurrent.futures.wait(futures)
    logger.info("Finished!")
```
