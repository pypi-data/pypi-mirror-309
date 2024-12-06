
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from awsglue.transforms import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
from pyspark.sql.types import StringType
import unicodedata
import re


from .logger import Logger
from .constant import DEFAULT_USER_NAME
from .enums import Environment, CommonColumns as Columns

"""
Use for define utils for Glue and pyspark
"""


def load_context(app_name='etl_practice', master='local[*]', environment=Environment.AWS_GLUE.value):
    """Start spark

    Args:
        app_name (str, optional): app name. Defaults to 'etl_practice'.
        master (str, optional): master. Defaults to 'local[*]'.

    Returns:
        glue_context, spark_sess, spark_logger, s3 (optional)
    """
    if environment == Environment.LOCAL.value:
        spark_builder = SparkSession.builder.master(master).appName(app_name)

        # spark session and logger
        spark = spark_builder.getOrCreate()
        logger = Logger()
        # glue_context = GlueContext(spark.sparkContext)

        return None, spark, logger, None

    spark_context = SparkContext()
    glue_context = GlueContext(spark_context)
    spark = glue_context.spark_session
    glue_logger = glue_context.get_logger()

    s3 = boto3.client('s3')

    return glue_context, spark, glue_logger, s3


def setup_aws_job(glue_context, job_name, args):
    """
    Initializes the AWS Glue Job for managing commits and other Glue job configurations.

    Parameters:
    - glue_context: GlueContext object.
    - job_name (str): Name of the AWS Glue job.
    - args (dict): Arguments for the AWS Glue job.
    """
    job = Job(glue_context)
    job.init(job_name, args)
    return job


def add_extra_data(df: DataFrame):
    """Add extra data to the DataFrame

    Args:
        df (DataFrame): Input DataFrame

    Returns:
        DataFrame: DataFrame with added extra data
    """
    # Add extra data to the DataFrame
    current = F.current_timestamp()
    df = (df.withColumn(Columns.HASHCODE.value, F.sha2(F.concat(*[F.col(c) for c in df.columns]), 256))
          .withColumn(Columns.CREATE_AT.value, current)
          .withColumn(Columns.UPDATE_AT.value, current)
          .withColumn(Columns.EFFECTIVE_FROM.value, current)
          .withColumn(Columns.IS_ACTIVE.value, F.lit(True))
          .withColumn(Columns.CREATE_BY.value, F.lit(DEFAULT_USER_NAME))
          .withColumn(Columns.UPDATE_BY.value, F.lit(DEFAULT_USER_NAME)))
    df = df.withColumn(Columns.HASHCODE.value, F.sha2(
        F.concat(*[F.col(c) for c in df.columns]), 256))
    return df


def build_column_date(year: int, month: int, day: int = 1):
    date_string = f"{year}-{month}-{day}"
    return F.to_date(F.lit(date_string), 'yyyy-M-d')


# Prefix normalize change name
NORMALIZE_CHANGE_NAME = "normalize_"
REGEX_NORMAL_CHARACTER = r'[^a-zA-Z0-9\s]'
REGEX_MULTI_SPACES = r'\s+'
EMPTY_CHARACTER = ''
SINGLE_SPACE_CHARACTER = ' '


def normalize_unicode(text):
    """
    Normalize Unicode text by removing accents.

    :param text: The text to normalize.
    :return: The normalized text with accents removed.
    """
    if text is None:
        return None
    # Normalize the text to NFD (Normalization Form Decomposition)
    text = unicodedata.normalize('NFD', text)
    # Remove combining characters (accents)
    return EMPTY_CHARACTER.join(c for c in text if not unicodedata.combining(c))


def normalize_columns(df: DataFrame, columns, is_change_name=False):
    """
    Clean a list of columns in a PySpark DataFrame by removing special characters, handling multiple spaces,
    converting to lowercase, and normalizing Unicode.

    :param df: The PySpark DataFrame.
    :param columns: A list of column names to clean.
    :return: A DataFrame with cleaned columns.
    """
    # Register the UDF
    normalize_unicode_udf = F.udf(normalize_unicode, StringType())
    for column in columns:
        # Check if the column name needs to be changed
        column_name = column
        if is_change_name:
            column_name = NORMALIZE_CHANGE_NAME + column
        # Normalize Unicode (remove accents)
        df = df.withColumn(column_name, normalize_unicode_udf(F.col(column)))
        # Remove non-alphanumeric characters (except spaces)
        df = df.withColumn(column_name, F.regexp_replace(
            F.col(column), REGEX_NORMAL_CHARACTER, SINGLE_SPACE_CHARACTER))
        # Replace multiple spaces with a single space
        df = df.withColumn(column_name, F.regexp_replace(
            F.col(column), REGEX_MULTI_SPACES, SINGLE_SPACE_CHARACTER))
        # Convert to lowercase
        df = df.withColumn(column_name, F.lower(F.trim(F.col(column))))

    return df


def normalize_string(input_string):
    """
    Clean a string by removing special characters, trimming whitespace, converting to lowercase, and normalizing Unicode.

    :param input_string: The string to clean.
    :return: A cleaned string.
    """
    if input_string is None:
        return None
    # Normalize Unicode (remove accents)
    normalized_str = normalize_unicode(input_string)
    # Remove non-alphanumeric characters (except spaces)
    normalized_str = re.sub(REGEX_NORMAL_CHARACTER,
                            SINGLE_SPACE_CHARACTER, normalized_str)
    # Replace multiple spaces with a single space
    normalized_str = re.sub(
        REGEX_MULTI_SPACES, SINGLE_SPACE_CHARACTER, normalized_str).strip()
    # Convert to lowercase
    normalized_str = normalized_str.lower()

    return normalized_str
