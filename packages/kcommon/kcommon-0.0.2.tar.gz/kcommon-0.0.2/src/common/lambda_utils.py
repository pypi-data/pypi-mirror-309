from __future__ import annotations
import json
import pandas as pd
import requests
from io import StringIO
import logging
import boto3
from botocore.exceptions import ClientError
from requests import Response

from .enums import CommonColumns as Columns, ReponseHeader, StatusCode

"""
Use for define utils for Lambda
"""


def transform_column_name(df: pd.DataFrame, columns_info: dict) -> pd.DataFrame:
    """Transform dataframe header

    Args:
        df (pd.DataFrame): The DataFrame to transform.
        columns_list (list): A list of dictionaries with 'old_column' and 'new_column' keys.

    Returns:
        pd.DataFrame: The DataFrame after transformation.
    """
    # Create a dictionary for renaming columns
    rename_dict = {old_col: new_col for old_col, new_col in zip(columns_info.get(
        Columns.RAW_COLUMNS.value), columns_info.get(Columns.NEW_COLUMNS.value))}

    # Rename the columns
    df = df.rename(columns=rename_dict)
    return df.reindex(columns=columns_info.get(Columns.TARGET_COLUMNS.value))


def tranform_array_data(df: pd.DataFrame, columns: list[str]):
    for i in columns:
        df[i] = df[i].apply(lambda x: ', '.join(x))


def upload_to_s3(df: pd.DataFrame, file_name: str, bucket: str):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_resource = boto3.resource('s3')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, header=True)
    try:
        s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())
    except ClientError as e:
        logging.error(e)
        return False
    return True


def replace_values(df: pd.DataFrame, col: str, replace_rules: list[dict]):
    for rules in replace_rules:
        df[col] = df[col].replace(rules["old_name"], rules["new_name"])


def create_df(data: list[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the provided data.

    Args:
        data (list[dict]): A list of dictionaries representing the data.

    Returns:
        pd.DataFrame: The created DataFrame.
    """
    return pd.DataFrame(data)


def handle_get_pageable(url: str, headers: dict, query_params: dict) -> dict:

    response: Response = requests.get(url, headers=headers,
                                      data=json.dumps(query_params), verify=False)

    res_headers = response.headers
    total_page = res_headers.get(ReponseHeader.X_TOTAL_PAGE.value)
    total_count = res_headers.get(ReponseHeader.X_TOTAL_COUNT.value)
    current_page = res_headers.get(ReponseHeader.X_CURRENT_PAGE.value)

    if response.status_code == StatusCode.SUCCESS.value:

        items: list[dict] = response.json()
        data: dict = {
            "items": items,
            "page_count": total_page,
            "total_count": total_count,
            "newPage": int(current_page) < int(total_page)
        }

        return data

    else:
        raise Exception(
            f"Error fetching data from {url}: {response.status_code} - {response.text}")


def handle_get_detail(url: str, headers: dict, query_params: dict) -> dict:
    response: Response = requests.get(
        url, headers=headers, data=json.dumps(query_params), verify=False)
    if response.status_code == StatusCode.SUCCESS.value:
        return response.json()
    else:
        raise Exception(
            f"Error fetching data from {url}: {response.status_code} - {response.text}")
