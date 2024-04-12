"""
Exceptions that can be raised by the storage package.
"""


# Cloud Storage Errors
class BlobNotFoundError(Exception):
    pass


class BlobAlreadyExistsError(Exception):
    pass
