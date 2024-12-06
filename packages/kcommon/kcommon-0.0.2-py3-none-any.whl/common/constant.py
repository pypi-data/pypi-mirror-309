from __future__ import annotations
from typing import Dict, TypeAlias, List

#### SIMPLE CONSTANT VALUES ####

MONTH_RANGE = {
    "Jan": "Dec-Jan",
    "Feb": "Feb-Mar",
    "Mar": "Feb-Mar",
    "Apr": "Apr-May",
    "May": "Apr-May",
    "Jun": "Jun-Jul",
    "Jul": "Jun-Jul",
    "Aug": "Aug-Sep",
    "Sep": "Aug-Sep",
    "Oct": "Oct-Nov",
    "Nov": "Oct-Nov",
    "Dec": "Dec-Jan"
}

DEFAULT_USER_NAME = "GLUE_JOB"

YEAR_MONTH_DAY_FORMAT = "yyyy-MM-dd"
FULL_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

WORKPLACE_FATALITY = [
    "fatal", "aerodrome occurrence\n(affecting aircraft operations)", "aerodrome occurrence (affecting aircraft operations)"]
WORKPLACE_DANGEROUS = [
    "major injury", "aerodrome occurrence\n(not affecting aircraft operations)", "near miss", "aerodrome occurrence (not affecting aircraft operations)",
    "occupational diseases", "dangerous occurences"]
WORKPLACE_DAMAGE = ["first aid", "minor injury",
                    "property / service damage (landside)", "work related traffic incident"]

DEFAULT_SPLIT_ARRAY_VALUE = ", "

#### FOR DATA TYPES ####

SheetMetadataItem: TypeAlias = Dict[str, str | List[str]]
SheetMetadata: TypeAlias = List[SheetMetadataItem]


#### FOR CONFIG INFO ####


# for redshift config
LOAD_SUBCON_REDSHIFT_INFO = {
    "redshift_options": {
        "url": "jdbc:redshift://your-cluster-endpoint:5439/your_database",
        "dbtable": "your_redshift_table",
        "user": "your_username",
        "password": "your_password",
        "redshiftTmpDir": "s3://your-temp-dir/",
    },
    "select_columns": []
}


REDSHIFT_SECRET_NAME = "cag-redshift-credential"
REGION_NAME = "ap-southeast-1"
