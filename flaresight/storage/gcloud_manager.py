"""
Managing Google Cloud Storage Blobs
"""
# standard library imports
import os

# current package imports
from .gcloud_blob import GCloudBlob

# local imports
from filesys.file import File

# 3rd party imports
from google.cloud import storage


class GCloudBlobManager:
    """
    A class to manage Blobs in Google Cloud Storage.
    """

    def __init__(self) -> None:
        """
        Initializes a GCloudBlobStorageManager object

        Parameters
        ----------
        None
        """
        self._client = storage.Client()

    def _get_bucket(self, bucket_name: str) -> storage.Bucket:
        """
        Returns a storage.Bucket object for a given bucket name

        Parameters
        ----------
        bucket_name: str
            Name of the bucket to retrieve

        Returns
        -------
        storage.Bucket
            The bucket object for the given bucket name
        """
        return self._client.bucket(bucket_name)

    def _get_blob(self, bucket_name: str, blob_path: list[str]) -> storage.Blob:
        """
        Returns a storage.Blob object for a given blob path

        Parameters
        ----------
        bucket_name: str
            Name of the bucket where the blob is located
        blob_path: list[str]
            Complete path within the bucket where the blob is stored
            Ex: ['006ek4HPQjRW9o2UbfvLyGIedaz2', '564cfa8e-45eb-4ec4-9f55-fc5cead468aa',
                '05654cce-fcb0-4a36-a257-cf118abc610a']

        Returns
        -------
        storage.Blob
            The blob object for the given blob path
        """
        return storage.Blob(
            bucket=self._get_bucket(bucket_name), name=os.path.join(*blob_path)
        )

    def upload(
        self,
        file: File,
        bucket_name: str,
        blob_path: list[str],
        overwrite: bool = False,
    ) -> GCloudBlob:
        """
        Uploads 'file' to Google Cloud Storage bucket 'bucket_name' at 'blob_path'.

        Parameters
        ----------
        file: File
            The file to upload
        bucket_name: str
            Name of the bucket to upload the file to
        blob_path: list[str]
            Complete path within the bucket where to store 'file'
            Ex: ['006ek4HPQjRW9o2UbfvLyGIedaz2', '564cfa8e-45eb-4ec4-9f55-fc5cead468aa',
                '05654cce-fcb0-4a36-a257-cf118abc610a']
        overwrite: bool = False
            Overwrites any existing blob's if True

        Returns
        -------
        GCloudBlob
            The blob object in Cloud Storage of the uploaded file
        """
        if overwrite is False:
            GCloudBlob(bucket_name, blob_path).assert_does_not_exist()

        # upload blob (these are Google's defined blobs)
        blob = self._get_blob(bucket_name, blob_path)
        blob.upload_from_filename(file.path, num_retries=3)

        # return blob (our defined blobs)
        blob = GCloudBlob(bucket_name, blob_path)
        blob.assert_exists()
        return blob

    def make_empty_dir(
        self,
        bucket_name: str,
        dir_path: list[str],
    ) -> None:
        """
        Creates a new, empty directory at 'dir_path' in Cloud Storage bucket
        'bucket_name'

        Parameters
        ----------
        bucket_name: str
            Name of the bucket to create the directory in
        dir_path: str
            Absolute path within the bucket where to create the directory

        Returns
        -------
        None
        """
        blob = self._get_blob(bucket_name, dir_path)
        blob.upload_from_string(
            "", content_type="application/x-www-form-urlencoded;charset=UTF-8"
        )

    def delete_dir(self, bucket_name: str, dir_path: str) -> None:
        """
        Deletes all blobs and directories within 'dir_path' in Google Cloud Storage
        bucket 'bucket_name'.

        Parameters
        ----------
        bucket_name: str
            Name of the bucket from which the directory is deleted
        dir_path: str
            Absolute path within the bucket where the directory is located

        Returns
        -------
        None
        """
        bucket = self._get_bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=os.path.join(*dir_path)))
        bucket.delete_blobs(blobs)
