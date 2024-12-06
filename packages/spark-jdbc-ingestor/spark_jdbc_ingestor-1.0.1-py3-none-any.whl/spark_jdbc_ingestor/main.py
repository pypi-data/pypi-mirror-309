import logging
from datetime import datetime
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.window import Window


class JdbcIngestor:
    """
    A class to handle JDBC ingestion from a SQL database.

    Attributes:
    spark: Spark instance
    url (str): The JDBC URL for the database connection.
    user (str): The username for the database connection.
    password (str): The password for the database connection.
    driver (str): The JDBC driver class name.
    isolation_level (str): The transaction isolation level. Default is 'READ_COMMITTED'.
    fetch_size (int): The number of rows to fetch at a time. Default is 10000.
    """

    def __init__(
        self,
        spark,
        url: str,
        user: str,
        password: str,
        driver: str,
        isolation_level: str = "READ_COMMITTED",
        fetch_size: int = 10000,
    ):
        """
        Initializes the JdbcIngestion class with the given parameters.

        Args:
        spark: Spark instance
        url (str): The JDBC URL for the database connection.
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        driver (str): The JDBC driver class name.
        isolation_level (str): The transaction isolation level. Default is 'READ_COMMITTED'.
        fetch_size (int): The number of rows to fetch at a time. Default is 10000.
        """
        self.spark = spark
        self.url = url
        self.user = user
        self.password = password
        self.driver = driver
        self.isolation_level = isolation_level
        self.fetch_size = fetch_size
        self.logger = logging.getLogger(__name__)

    def from_table(self, table: str):
        """
        Creates a query to select all data from the specified table.

        Args:
        table (str): The name of the table to select data from.

        Returns:
        JdbcIngestion._From: An instance of the _From class with the specified table query.
        """
        return self._From(self, self.spark, f"(select * from {table}) as source_table")

    def from_query(self, query: str):
        """
        Creates a query from the specified SQL query string.

        Args:
        query (str): The SQL query string.

        Returns:
        JdbcIngestion._From: An instance of the _From class with the specified query.
        """
        return self._From(self, self.spark, query)

    def execute(self, query):
        """
        Executes the specified SQL query.

        Args:
        query (str): The SQL query string to execute.

        Returns:
        DataFrame: A Spark DataFrame containing the results of the query.
        """
        return self._From(self, self.spark, None).execute(query)

    def get_last_value(self, table: str, column: str, default_value=None):
        """
        Retrieves the last value of a specified column from a table.

        Args:
        table (str): The name of the table to query.
        column (str): The column to retrieve the last value from.
        default_value (optional): The default value to return if no value is found. Default is None.

        Returns:
        The last value of the specified column if found, otherwise the default value.
        """
        return self._LastValue(self, self.spark, table, column, default_value).execute()

    class _From:
        """
        A helper class to handle the construction and execution of queries.

        Attributes:
        parent (JdbcIngestion): The parent JdbcIngestion instance.
        spark: Spark instance
        query (str): The SQL query string.
        filters (list): A list of filters to apply to the query.
        """

        def __init__(self, parent, spark, query: str):
            """
            Initializes the _From class with the given parameters.

            Args:
            parent (JdbcIngestion): The parent JdbcIngestion instance.
            spark: Spark instance
            query (str): The SQL query string.
            """
            self.parent = parent
            self.spark = spark
            self.query = query
            self.filters = []

        def add_filter(self, col: str):
            """
            Adds a filter to the query.

            Args:
            col (str): The filter condition to add.

            Returns:
            JdbcIngestion._From: The current instance of the _From class.
            """
            self.filters.append(col)
            return self

        def _create_read(self):
            """
            Creates a Spark DataFrame reader with the JDBC options.

            Returns:
            DataFrameReader: A Spark DataFrame reader configured with the JDBC options.
            """
            return (
                self.spark.read.format("jdbc")
                .option("url", self.parent.url)
                .option("driver", self.parent.driver)
                .option("user", self.parent.user)
                .option("password", self.parent.password)
                .option("fetchsize", self.parent.fetch_size)
                .option("isolationLevel", self.parent.isolation_level)
            )

        def with_last_value(self, table: str, column: str, default_value=None):
            """
            Adds a filter to the query based on the last value of a specified column in a table.

            Args:
            table (str): The name of the table to get the last value from.
            column (str): The column to get the last value from.
            default_value (optional): The default value to use if no value is found. Default is None.

            Returns:
            JdbcIngestion._From: The current instance of the _From class with the added filter.
            """
            _last_value = self.parent._LastValue(
                self, self.spark, table, column, default_value).execute()
            match _last_value:
                case str():
                    return self.add_filter(f"{column} > '{_last_value}'")
                case datetime():
                    return self.add_filter(f"{column} > '{_last_value}'")
                case _:
                    return self.add_filter(f"{column} > {_last_value}")

        def _prepare(
            self,
            partition_column: str = None,
            num_partitions: int = 8,
            lower_bound=None,
            upper_bound=None,
        ):
            """
            Prepares the query for execution by setting up partitioning and boundaries.

            Args:
            partition_column (str, optional): The column to partition the data on. Default is None.
            num_partitions (int, optional): The number of partitions to create. Default is 8.
            lower_bound (optional): The lower bound of the partition column. Default is None.
            upper_bound (optional): The upper bound of the partition column. Default is None.

            Returns:
            DataFrameReader: A Spark DataFrame reader configured with the query and partitioning options.
            """
            reader = self._create_read()
            _query = self.query
            _filters = self.filters

            if len(_filters) > 0:
                _query = f"(select * from {_query} where {' and '.join(_filters)}) as filtered_source_table"

            if not partition_column is None:
                if lower_bound is None or upper_bound is None:
                    boundaries_query = (
                        f"(select min({partition_column}) as lower_bound, max({partition_column}) as upper_bound"
                        + f" from {_query}) as boundaries"
                    )
                    self.parent.logger.info(
                        f"Looking for boundaries: {boundaries_query}")
                    boundaries = (
                        self._create_read().option("dbtable", boundaries_query).load()
                    ).first()
                    lower_bound = boundaries["lower_bound"]
                    upper_bound = boundaries["upper_bound"]
                    self.parent.logger.info(
                        f"Found boundaries: lower_bound={lower_bound}, upper_bound={upper_bound}"
                    )
                if lower_bound is not None and upper_bound is not None:
                    reader = (
                        reader.option("partitionColumn", partition_column)
                        .option("lowerBound", boundaries["lower_bound"])
                        .option("upperBound", boundaries["upper_bound"])
                        .option("numPartitions", num_partitions)
                    )
            self.parent.logger.info(f"Executing query: {_query}")
            return reader.option("dbtable", _query)

        def load(
            self,
            partition_column: str = None,
            num_partitions: int = 8,
            lower_bound=None,
            upper_bound=None,
        ):
            """
            Loads data from the query into a Spark DataFrame.

            Args:
            partition_column (str, optional): The column to partition the data on. Default is None.
            num_partitions (int, optional): The number of partitions to create. Default is 8.
            lower_bound (optional): The lower bound of the partition column. Default is None.
            upper_bound (optional): The upper bound of the partition column. Default is None.

            Returns:
            DataFrame: A Spark DataFrame containing the results of the query.
            """
            return self.parent._To(self, self.spark, self._prepare(partition_column, num_partitions, lower_bound, upper_bound).load())

        def execute(self, query: str):
            """
            Executes the specified SQL query and loads the results into a Spark DataFrame.

            Args:
            query (str): The SQL query string to execute.

            Returns:
            DataFrame: A Spark DataFrame containing the results of the query.
            """
            """
            Executes the specified SQL query and loads the results into a Spark DataFrame.

            Args:
            query (str): The SQL query string to execute.

            Returns:
            DataFrame: A Spark DataFrame containing the results of the query.
            """
            self.parent.logger.info(f"Executing query: {query}")
            return self._create_read().option("dbtable", query).load()

        def analyze(self, sample=1000):
            return self.parent._TableAnalyzer(self, self.spark, self._prepare().load()).analyze_table(sample=sample)

    class _TableAnalyzer:
        """
        A class used to analyze a Spark DataFrame and compute various statistics.

        Attributes
        ----------
        spark: Spark instance
        df : DataFrame
            The Spark DataFrame to be analyzed.

        Methods
        -------
        _is_numeric_field(field)
            Checks if a field is of a numeric data type.

        _is_temporal_field(field)
            Checks if a field is of a temporal data type.

        _get_stats()
            Computes statistics for numeric and temporal fields in the DataFrame.

        analyze_table(sample=1000)
            Analyzes the DataFrame and returns a DataFrame with computed statistics.
        """

        def __init__(self, parent, spark, df):
            """
            Initializes the _TableAnalyzer class with the given parameters.

            Args:
            parent (JdbcIngestion._From): The parent _From instance.
            spark: Spark instance
            df (DataFrame): The Spark DataFrame to be analyzed.
            """

            self.parent = parent
            self.spark = spark
            self.df = df

        def _is_numeric_field(self, field):
            """
            Checks if a field is of a numeric data type.

            Parameters
            ----------
            field : StructField
                The field to be checked.

            Returns
            -------
            bool
                True if the field is of a numeric data type, False otherwise.
            """
            return isinstance(
                field.dataType,
                (
                    ByteType,
                    ShortType,
                    IntegerType,
                    LongType,
                    FloatType,
                    DoubleType,
                    DecimalType,
                ),
            )

        def _is_temporal_field(self, field):
            """
            Checks if a field is of a temporal data type.

            Parameters
            ----------
            field : StructField
                The field to be checked.

            Returns
            -------
            bool
                True if the field is of a temporal data type, False otherwise.
            """
            return isinstance(field.dataType, (DateType, TimestampType))

        def _get_stats(self, sample):
            """
            Computes statistics for numeric and temporal fields in the DataFrame.

            Parameters
            ----------
            sample : int
                The number of rows to sample from the DataFrame for analysis.

            Returns
            -------
            DataFrame
                A DataFrame containing computed statistics for numeric and temporal fields.
            """
            analyze_df = self.df.limit(sample)
            select_fields = []
            for field in self.df.schema.fields:
                field_name = field.name
                for stat_name in ["min", "max", "avg", "stddev", "count"]:
                    if self._is_numeric_field(field):
                        select_fields.append(
                            f"{stat_name}({field_name}) as {stat_name}___{field_name}"
                        )
                    elif self._is_temporal_field(field):
                        select_fields.append(
                            f"{stat_name}(unix_timestamp({field_name})) as {stat_name}___{field_name}"
                        )
                if self._is_numeric_field(field) or self._is_temporal_field(field):
                    select_fields.append(
                        f"count(distinct {field_name}) as count_distinct___{field_name}")
            return analyze_df.selectExpr(*select_fields)

        def analyze_table(self, sample=1000):
            """
            Analyzes the DataFrame and returns a DataFrame with computed statistics.

            Parameters
            ----------
            sample : int, optional
                The number of rows to sample from the DataFrame for analysis (default is 1000).

            Returns
            -------
            DataFrame
                A DataFrame containing computed statistics ordered for stddev, uniformity and 
                completeness metrics.
            """
            stats_df = self._get_stats(sample)
            self.parent.parent.logger.info(
                f"Getting statistical data from table (sample={sample})...")
            stats_values = stats_df.collect()[0]
            data = {}
            stats_functs = ["min", "max", "avg",
                            "stddev", "count", "count_distinct"]
            fields = []
            for field in stats_df.schema.fields:
                stat_name, field_name = field.name.split("___")
                if (field_name not in fields):
                    fields.append(field_name)
                if field_name not in data:
                    data[field_name] = [field_name] + [0] * len(stats_functs)
                data[field_name][stats_functs.index(
                    stat_name)+1] = stats_values[f"{stat_name}___{field_name}"]
                window_spec = Window.partitionBy("dummy").orderBy("dummy")
            return (
                self.spark.createDataFrame([x for x in tuple(data.values())], [
                                           "field_name"] + [sf for sf in stats_functs])
                    .withColumn("uniformity", expr(f"(count_distinct/{sample})"))
                    .withColumn("completeness", expr(f"(count/{sample})"))
                    .orderBy(desc("uniformity"), desc("completeness"), asc("stddev"))
                    .withColumn("dummy", lit(1))
                    .withColumn("ranking", row_number().over(window_spec))
                    .drop("dummy")
                    .select("ranking", "field_name", *stats_functs, "uniformity", "completeness")
            )

    class _To:
        """
        A helper class to handle the writing of DataFrames to tables.

        Attributes:
        parent (JdbcIngestion._From): The parent _From instance.
        spark: Spark instance
        df (DataFrame): The Spark DataFrame to be written.
        """

        def __init__(self, parent, spark, df):
            """
            Initializes the _To class with the given parameters.

            Args:
            parent (JdbcIngestion._From): The parent _From instance.
            spark: Spark instance
            df (DataFrame): The Spark DataFrame to be written.
            """
            self.parent = parent
            self.spark = spark
            self.df = df

        def append(self, table: str):
            """
            Appends the DataFrame to the specified table.

            Args:
            table (str): The name of the table to append the data to.

            Returns:
            None
            """
            return self.df.write.mode("append").saveAsTable(table)

        def overwrite(self, table: str):
            """
            Overwrites the specified table with the DataFrame.

            Args:
            table (str): The name of the table to overwrite with the data.

            Returns:
            None
            """
            return self.df.write.mode("overwrite").saveAsTable(table)

    class _LastValue:
        """
        A helper class to retrieve the last value of a specified column from a table.

        Attributes:
        parent (JdbcIngestion): The parent JdbcIngestion instance.
        spark: Spark instance
        table (str): The name of the table to query.
        column (str): The column to retrieve the last value from.
        default_value (optional): The default value to return if no value is found. Default is None.
        """

        def __init__(self, parent, spark, table: str, column: str, default_value=None):
            """
            Initializes the _LastValue class with the given parameters.

            Args:
            parent (JdbcIngestion): The parent JdbcIngestion instance.
            spark: Spark instance
            table (str): The name of the table to query.
            column (str): The column to retrieve the last value from.
            default_value (optional): The default value to return if no value is found. Default is None.
            """
            self.parent = parent
            self.spark = spark
            self.table = table
            self.column = column
            self.default_value = default_value

        def execute(self):
            """
            Executes the query to retrieve the last value of the specified column from the table.

            Returns:
            The last value of the specified column if found, otherwise the default value.
            """
            result = (
                self.spark.read.table(self.table)
                .select(max(self.column))
                .collect()[0][0]
            )
            return result if result is not None else self.default_value
