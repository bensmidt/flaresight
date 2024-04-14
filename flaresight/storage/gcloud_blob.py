"""
Working with Google Cloud Blobs.
"""
# standard library imports
from datetime import datetime, timedelta, timezone
import logging
import os

# current package imports
from .exceptions import (
    BlobAlreadyExistsError,
    BlobNotFoundError,
)

# local package imports
from filesys.dir import Dir
from filesys.file import File
from utils.secrets import Secrets

# 3rd party imports
from google.cloud import storage
import google.auth
from google.auth.transport import requests


class GCloudBlob:
    """
    A class to represent and interact with Google Cloud Blobs.
    """

    def __init__(self, bucket_name: str, path: list[str]) -> None:
        """
        Initialize GCloudBlob

        Parameters
        ----------
        bucket_name: str
            Name of the bucket the blob is located in
        path: list[str]
            Complete path within the bucket where the blob is stored

        Returns
        -------
        None
        """
        self._path = path

        self._client = storage.Client()
        self._bucket = self._client.bucket(bucket_name)
        self._blob = storage.Blob(bucket=self._bucket, name="/".join(self._path))
        self._service_account_email = Secrets().GCLOUD_SERVICE_ACCOUNT_EMAIL

    @property
    def bucket(self) -> str:
        """
        Returns the bucket of the blob.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The bucket of the blob.
        """
        return self._bucket.name

    @property
    def path(self) -> str:
        """
        Returns the path of the blob.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The path of the blob.
        """
        return self._path

    @property
    def public_url(self) -> str:
        """
        Returns the public url of the blob.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The public url of the blob.
        """
        return self._blob.public_url

    @property
    def uri(self) -> str:
        """
        Returns the uri of the blob in Cloud Storage

        Parameters
        ----------
        None

        Returns
        -------
        str
            The uri of the blob.
        """
        return "gs://{}/{}".format(self._bucket.name, self._blob.name)

    def check_exists(self) -> str or None:
        """
        Checks if Blob exists in Cloud Storage. Returns None if so, a descriptive error
        message if not.

        Parameters
        ----------
        None

        Returns
        -------
        str or None
            None if Blob exists in Cloud Storage, a descriptive error message if not.
        """
        if not self._blob.exists(self._client):
            return "Blob '{}' does not exist in bucket '{}'.".format(
                self._path, self._bucket.name
            )

        return None

    def exists(self) -> bool:
        """
        Returns True if Blob exists in Cloud Storage, False if not.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if Blob exists, False if not.
        """
        return self.check_exists() is None

    def assert_exists(self) -> None:
        """
        Raises an error if Blob does not exist in Cloud Storage.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        BlobNotFoundError
            If Blob does not exist in Cloud Storage.
        """
        error = self.check_exists()
        if error is not None:
            raise BlobNotFoundError(error)

    def check_does_not_exist(self) -> str or None:
        """
        Checks that a blob does not exist in Cloud Storage bucket 'bucket_name' at
        'blob_path'. Returns None if a blob does not exist, a descriptive error message
        if a blob does exist.

        Parameters
        ----------
        None

        Returns
        -------
        str or None
            None if a blob does not exist in Cloud Storage bucket 'bucket_name' at
            'blob_path', a descriptive error message if a blob does exist.
        """
        if self.exists():
            return "Blob '{}' already exists in bucket '{}'".format(
                self._path, self._bucket.name
            )
        return None

    def assert_does_not_exist(self) -> None:
        """
        Raises an error if Blob exists in Cloud Storage.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        BlobAlreadyExistsError
            If Blob exists in Cloud Storage.
        """
        error = self.check_does_not_exist()
        if error is not None:
            raise BlobAlreadyExistsError(error)

    def download(self, file_path: str) -> File:
        """
        Downloads the Blob to local device at 'file_path'

        Parameters
        ----------
        file_path: str
            Absolute file path on local device where the blob is downloaded to

        Returns
        -------
        File
            The downloaded blob as a local file object
        """
        self.assert_exists()

        # download blob
        self._blob.download_to_filename(file_path)

        # return as File object
        file = File(file_path)
        file.assert_exists()
        return file

    def upload(self, file: File, overwrite: bool = True) -> None:
        """
        Uploads a file to Cloud Storage at the blob's specified path in Cloud Storage.

        Parameters
        ----------
        file: File
            The file to upload to Cloud Storage.
        overwrite: bool = False
            Overwrites any existing blob's if True.

        Returns
        -------
        None
        """
        if overwrite is False:
            self.assert_does_not_exist()

        self._blob.upload_from_filename(file.path, num_retries=3)
        self.assert_exists()

    def upload_dir(
        self, dir: Dir, overwrite: bool = True, upload_hidden: bool = False
    ) -> None:
        """
        Uploads a directory to Cloud Storage at the blob's specified path in Cloud Storage.

        Parameters
        ----------
        dir: Dir
            The directory to upload to Cloud Storage.
        overwrite: bool = False
            Overwrites any existing blob's if True.
        upload_hidden: bool = False
            Whether to upload hidden files and directories.

        Returns
        -------
        None
        """
        for subdir in dir.get_subdirs():
            if subdir.is_hidden() and not upload_hidden:
                continue
            # create subdirectory in Cloud Storage
            blob = GCloudBlob(self._bucket.name, self._path + [subdir.get_name()])
            blob.upload_dir(subdir, overwrite=overwrite)
        for file in dir.get_files():
            if file.is_hidden() and not upload_hidden:
                continue
            blob = GCloudBlob(self._bucket.name, self._path + [file.get_name()])
            blob.upload(file, overwrite=overwrite)

    def delete(self) -> None:
        """
        Deletes a blob from Google Cloud Storage bucket 'bucket_name' at 'blob_path'.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # exit function if blob already doesn't exist
        if self.exists() is False:
            msg = (
                "Cannot delete blob '{}' since it does not exist in bucket '{}'."
                "".format(self._path, self._bucket.name)
            )
            logging.warning(msg)
            return None

        # delete blob
        self._blob.delete()

    def _get_signed_url(
        self,
        expiration_duration_secs: int,
        download: bool = False,
        download_title: str = None,
        download_file_extension: str = None,
    ) -> str or None:
        """
        Generates a signed URL for viewing or downloading Blob.

        Parameters
        ----------
        expiration_duration_secs: int
            Expiration duration for the signed url in seconds
        download: bool
            True to use signed url for downloading, False to use signed url for viewing
        download_title: str
            Name of the file when downloading with signed url
        download_file_extension: str
            File type of the file (mp4, txt, etc.) when downloading with signed url

        Returns
        -------
        str
            The signed url used to view or download a blob
        """
        self.assert_exists()

        # Perform a refresh request to get the access token of the current credentials
        credentials, _ = google.auth.default()
        r = requests.Request()
        credentials.refresh(r)

        # set the title and file extension if blob is being downloaded
        if download is True:
            response_disposition = (
                "attachment; filename={}.{}"
                "".format(download_title, download_file_extension)
            )
        else:
            response_disposition = None

        # generate signed url
        expiration_date = datetime.now(timezone.utc) + timedelta(
            seconds=expiration_duration_secs
        )
        signed_url = self._blob.generate_signed_url(
            expiration=expiration_date,
            service_account_email=Secrets().GCLOUD_SERVICE_ACCOUNT_EMAIL,
            access_token=credentials.token,
            method="GET",
            response_disposition=response_disposition,
        )
        return signed_url

    def get_viewable_signed_url(self, expiration_duration_secs: int) -> str:
        """
        Generates a signed URL for viewing Blob.

        Parameters
        ----------
        expiration_duration_secs: int
            Expiration duration for the signed url in seconds

        Returns
        -------
        str
            The signed url used to view Blob
        """
        self.assert_exists()
        return self._get_signed_url(expiration_duration_secs)

    def get_downloadable_signed_url(
        self,
        expiration_duration_secs: int,
        title: str,
        file_extension: str,
    ) -> str:
        """
        Generates a signed URL for downloading Blob.

        Parameters
        ----------
        expiration_duration_secs: int
            Expiration duration for the signed url in seconds
        title: str
            Name of the file when downloading with signed url
        file_extension: str
            File type of the file (mp4, txt, etc.) when downloading with signed url

        Returns
        -------
        str
            The signed url used to download Blob
        """
        self.assert_exists()
        return self._get_signed_url(
            expiration_duration_secs=expiration_duration_secs,
            download=True,
            download_title=title,
            download_file_extension=file_extension,
        )

    def get_mime_type(self) -> str:
        """
        Returns the mime type of the blob.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The mime type of the blob.
        """
        self.assert_exists()
        self._blob.reload()  # fetch metadata
        return self._blob.content_type

    def get_file_type(self) -> str:
        """
        Returns the file type of the blob.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The file type of the blob.
        """
        self.assert_exists()
        file_type, file_subtype = self.get_mime_type().split("/")
        return file_type

    def get_file_subtype(self) -> str:
        """
        Returns the file subtype of the blob.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The file subtype of the blob.
        """
        self.assert_exists()
        file_type, file_subtype = self.get_mime_type().split("/")
        return file_subtype

    def get_file_size(self) -> str:
        """
        Returns the file size in bytes of the blob.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The file size of the blob.
        """
        self.assert_exists()
        self._blob.reload()  # fetch metadata
        return self._blob.size
