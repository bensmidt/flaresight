"""
Google Cloud utility functions
"""
# standard library imports
from datetime import datetime

# third party imports
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import firebase_admin
from firebase_admin import credentials


def gcloud_DatetimeWithNanoseconds_to_datetime(
    gcloud_datetime: DatetimeWithNanoseconds,
) -> datetime:
    """
    Convert google.api_core.datetime_helpers.DatetimeWithNanoseconds to
    datetime.datetime

    Parameters
    ----------
    gcloud_datetime: google.api_core.datetime_helpers.DatetimeWithNanoseconds
        DatetimeWithNanoseconds object

    Returns
    -------
    datetime.datetime
        datetime.datetime object
    """
    python_datetime = datetime(
        gcloud_datetime.year,
        gcloud_datetime.month,
        gcloud_datetime.day,
        gcloud_datetime.hour,
        gcloud_datetime.minute,
        gcloud_datetime.second,
        gcloud_datetime.microsecond,
    )
    return python_datetime


def init_firebase() -> None:
    """
    Initialize firebase_admin app

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
