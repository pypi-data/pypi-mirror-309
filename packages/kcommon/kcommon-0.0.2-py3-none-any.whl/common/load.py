from __future__ import annotations
from pyspark.sql import DataFrame, SparkSession

from awsglue.transforms import *
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from .enums import FileType


def load_data(glue_context: GlueContext,
              df: DataFrame,
              file_type: FileType,
              csv_file_info=None,
              redshift_info=None):

    match file_type:

        case FileType.CSV_LOCAL:
            if csv_file_info is None:
                raise ValueError("csv_file_info parameter is required")
            output_path = csv_file_info.get("output_path")
            select_columns = csv_file_info.get("select_columns")

            if select_columns is not None and len(select_columns) > 0:
                df = df.select(*select_columns)

            df.repartition(1).write.mode("overwrite").csv(output_path, header=True)
        case FileType.CSV:
            if csv_file_info is None:
                raise ValueError("csv_file_info parameter is required")
            output_path = csv_file_info.get("output_path")
            select_columns = csv_file_info.get("select_columns")

            if select_columns is not None and len(select_columns) > 0:
                df = df.select(*select_columns)

            dynamic_frame = DynamicFrame.fromDF(
                df, glue_context, "dynamic_frame")
            glue_context.write_dynamic_frame.from_options(
                frame=dynamic_frame,
                connection_type='s3',
                connection_options={
                    'path': output_path,
                },
                format='csv',
                format_options={
                    "withHeader": True
                }
            )
        case FileType.REDSHIFT:
            if redshift_info is None:
                raise ValueError("redshift_info parameter is required")
            # get redshift connection info
            redshift_options = redshift_info.get("redshift_options")
            select_columns = redshift_info.get("select_columns")

            if select_columns is not None and len(select_columns) > 0:
                df = df.select(*select_columns)

            # convert dataframe to dynamicframe
            dynamic_frame = DynamicFrame.fromDF(
                df, glue_context, "dynamic_frame")

            # load data to redshift
            glue_context.write_dynamic_frame.from_options(
                frame=dynamic_frame,
                connection_type="redshift",
                connection_options=redshift_options
            )
        case _:
            raise ValueError("Type is not supported")
