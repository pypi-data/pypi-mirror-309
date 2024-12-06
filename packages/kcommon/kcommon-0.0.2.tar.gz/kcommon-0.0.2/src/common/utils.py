from __future__ import annotations
import os
from datetime import datetime, timedelta

import json
import boto3
from botocore.exceptions import ClientError

from .constant import MONTH_RANGE, DEFAULT_SPLIT_ARRAY_VALUE
from .enums import RequestParam, OsEnviron

"""
Use for define common utils, for all of modules
"""


def get_month_abbreviation(month: int):
    # List of month abbreviations
    month_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if 1 <= month <= 12:
        return month_abbr[month - 1]
    else:
        return "Invalid Month"


def get_current_remark(month: int = None, year: int = None):
    """Get the remark of month

    Returns:
        str: the current month's remark
    """
    # Get the current month and year
    if month is None and year is None:
        now = datetime.now()
        month = now.month
        year = now.year

    month_text = get_month_abbreviation(month)

    # Get the appropriate month range
    month_range = MONTH_RANGE[month_text]

    # Adjust the year if the range is "Dec-Jan" to roll over to the next year
    output_year = year if (
        month != "Dec") else year + 1
    return f"{month_range} {output_year}"


def datetime_to_date(date: datetime):
    """Get end of date

    Args:
        date (datetime): input date

    Returns:
        datetime: output date
    """
    return datetime(date.year, date.month, date.day)


def get_time_range(current_date: datetime):
    """
    Get the current time range in the format HH:00-HH:00.

    :return: A string representing the time range.
    """
    # Calculate the start of the current hour
    start_hour = current_date.replace(minute=0, second=0, microsecond=0)

    # Calculate the start of the next hour
    end_hour = start_hour + timedelta(hours=1)

    # Format the time range as HH:00-HH:00
    time_range = f"{start_hour.strftime('%H:00')}-{end_hour.strftime('%H:00')}"

    return time_range


def build_date(year: int, month: int, day: int = 1):
    return datetime(year, month, day)


def get_secret():
    region_name = os.environ.get(OsEnviron.REGION_NAME.value)
    secret_name = os.environ.get(OsEnviron.SECRET_NAME.value)

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        # logger.info(str(get_secret_value_response))
    except ClientError as e:
        raise e

    return json.loads(get_secret_value_response['SecretString'])


def get_redshift_info(secret_info, dbtable: str):
    return {
        "redshift_options": {
            "url": "jdbc:redshift://" + secret_info["host"] + ":" + str(secret_info["port"]) + "/" + secret_info["database"],
            "dbtable": dbtable,
            "user": secret_info["username"],
            "password": secret_info["password"],
            "redshiftTmpDir": "s3://cag-glue-data-temp/",
        }
    }


def generate_filename(event: dict, prefix: str, ext: str = "csv"):
    output_filename: str = event.get(RequestParam.OUTPUT_FILENAME.value)

    return f"{prefix}-{datetime.now().strftime('%Y%m%d')}.{ext}" if output_filename is None else output_filename


def transform_array_name(obj_data: list[dict], key: str):
    return DEFAULT_SPLIT_ARRAY_VALUE.join([p[key] for p in obj_data])
