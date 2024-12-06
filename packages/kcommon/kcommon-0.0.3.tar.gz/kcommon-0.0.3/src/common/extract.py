from pandas import ExcelFile
from pyspark.sql import SparkSession
import pandas as pd
from awsglue.context import GlueContext
from io import BytesIO
from .enums import FileType
from .constant import SheetMetadataItem, SheetMetadata


def extract_data(glue_context: GlueContext, spark: SparkSession,
                 file_type: FileType, s3=None,
                 csv_file_info=None,
                 excel_file_info=None,
                 redshift_options=None):
    """Extract Excel or CSV file with return CSV file contain data of selected columns

    Args:
        spark (SparkSession): spark session
        input_path (str): location of input file
        file_type (FileType): CSV or Excel
        columns (list[str], optional): if CSV file using this parameter. Defaults to None.
        sheet_metadata (SheetMetadata, optional): included sheets name and their columns (for Excel file). Defaults to None.

    Raises:
        ValueError: if the columns is None
        ValueError: if sheet_metadata is None
        Exception: if Type not supported

    Returns:
        None
    """
    match file_type:

        case FileType.CSV:
            if csv_file_info is None:
                raise ValueError("csv_file_info parameter is required")

            input_path = csv_file_info.get("input_path")
            select_raw_columns = csv_file_info.get("select_raw_columns")
            select_columns = csv_file_info.get("select_columns")

            df = glue_context.create_dynamic_frame.from_options(
                connection_type="s3",
                connection_options={"paths": [input_path]},
                format="csv",
                format_options={
                    "withHeader": True
                }
            )

            if select_raw_columns is not None:
                df = df.toDF().select(*select_raw_columns)

                for old_col, new_col in zip(df.columns, select_columns):
                    df = df.withColumnRenamed(old_col, new_col)
            else:
                df = df.toDF().select(*select_columns)

            return df

        case FileType.CSV_LOCAL:
            if csv_file_info is None:
                raise ValueError("csv_file_info parameter is required")

            input_path = csv_file_info.get("input_path")
            select_raw_columns = csv_file_info.get("select_raw_columns")
            select_columns = csv_file_info.get("select_columns")

            df = spark.read.csv(input_path, header=True,
                                inferSchema=True, multiLine=True, quote="\"", escape="\"")

            if select_raw_columns is not None:
                df = df.select(*select_raw_columns)

                for old_col, new_col in zip(df.columns, select_columns):
                    df = df.withColumnRenamed(old_col, new_col)
            else:
                df = df.select(*select_columns)

            return df

        case FileType.EXCEL:
            if excel_file_info is None:
                raise ValueError("excel_file_info parameter is required")

            bucket_name = excel_file_info.get("bucket_name")
            sheet_metadata = excel_file_info.get("sheet_metadata")
            input_path = excel_file_info.get("input_path")

            # Read the file from S3
            response = s3.get_object(Bucket=bucket_name, Key=input_path)
            data = response['Body'].read()

            read_file = pd.ExcelFile(BytesIO(data))
            return extract_excel_file(spark, read_file, sheet_metadata)

        case FileType.EXCEL_LOCAL:
            if excel_file_info is None:
                raise ValueError("excel_file_info parameter is required")

            sheet_metadata = excel_file_info.get("sheet_metadata")
            input_path = excel_file_info.get("input_path")

            read_file = pd.ExcelFile(input_path)
            return extract_excel_file(spark, read_file, sheet_metadata)

        case FileType.REDSHIFT:
            if redshift_options is None:
                raise ValueError("redshift_options parameter is required")

            redshift_connection_options = redshift_options.get(
                "redshift_options")
            columns = redshift_options.get("select_columns")

            # Create a DynamicFrame from the Redshift table
            redshift_dynamic_frame = glue_context.create_dynamic_frame.from_options(
                connection_type="redshift",
                connection_options=redshift_connection_options
            )

            df = redshift_dynamic_frame.toDF()
            if columns is not None and len(columns) > 0:
                df = df.select(*columns)
            # Convert DynamicFrame to Spark DataFrame
            return df
        case _:
            raise Exception("Type not supported")


def extract_excel_file(spark: SparkSession, read_file: ExcelFile, sheet_meta: SheetMetadata):
    """Extract data from excel file with list sheet

    Args:
        spark (SparkSession): spark session
        read_file (ExcelFile): file to read
        sheet_meta (SheetMetadata): sheets info

    Returns:
        List of DataFrame: all dataframe after read file
    """
    results = []
    for sheet_info in sheet_meta:
        df = read_excel_file(spark, read_file, sheet_info)
        results.append(df)
    return results


def read_excel_file(spark: SparkSession, excel_file: ExcelFile, sheet_info: SheetMetadataItem):
    """Read excel file

    Args:
        spark (SparkSession): spark session
        excel_file (ExcelFile): the input file
        sheet_info (SheetMetadataItem): sheet information need to read

    Returns:
        DataFrame: the dataframe after read
    """
    sheet_name = sheet_info.get("sheet_name")
    renamed_columns = sheet_info.get("renamed_columns")
    select_columns = sheet_info.get("select_columns")
    schema = sheet_info.get("schema")

    pd_df = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str)

    if schema is None:
        df = spark.createDataFrame(pd_df)
    else:
        df = spark.createDataFrame(pd_df, schema=schema)

    # rename to normalize df columns
    for old_col, new_col in zip(df.columns, renamed_columns):
        df = df.withColumnRenamed(old_col, new_col)

    return df.select(*select_columns)
