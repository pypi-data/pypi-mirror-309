from pyspark.sql import DataFrame
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BooleanType

def filter_data(input_df: DataFrame, config_df: DataFrame, spark, csv_file_info=None) -> DataFrame:
    """
    Filters the input DataFrame to exclude rows where the combination of values
    in the 'package' and 'subcontractor' columns match any pair in the exclusion config file.

    Args:
        input_df (DataFrame): The input DataFrame to be filtered.
        exclusion_config_path (str): The path to the CSV config file containing exclusion values.
        spark (SparkSession): The Spark session.
        exclusion_columns (list): A list of column names to apply the exclusion logic on (e.g., ['package', 'subcontractor']).

    Returns:
        DataFrame: The filtered DataFrame.
    """

    if csv_file_info is None:
                raise ValueError("csv_file_info parameter is required")

    exclusion_columns = csv_file_info.get("exclusion_columns")
    # Step 1: Get distinct pairs of (package, subcontractor) from the exclusion config
    exclusion_pairs = config_df.select(*exclusion_columns).distinct().collect()

    if not exclusion_pairs:
        # If the exclusion list is empty, return the original DataFrame as no exclusion is needed
        return input_df

    # Step 3: Convert the list of exclusion pairs into a set for fast lookup
    exclusion_set = set(tuple(row) for row in exclusion_pairs)

    # Step 4: Define a UDF to check if a given (package, subcontractor) combination is in the exclusion set
    def is_excluded(package, subcontractor):
        return (package, subcontractor) not in exclusion_set

    # Register the UDF
    exclusion_udf = udf(is_excluded, BooleanType())

    # Step 5: Apply the UDF to filter the DataFrame
    filtered_df = input_df.filter(exclusion_udf(col(exclusion_columns[0]), col(exclusion_columns[1])))


    return filtered_df