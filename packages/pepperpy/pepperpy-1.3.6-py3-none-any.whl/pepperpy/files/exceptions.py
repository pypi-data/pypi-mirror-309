"""File handling exceptions"""


class FileError(Exception):
    """Base file handling exception"""

    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause
