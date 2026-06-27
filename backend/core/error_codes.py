from enum import Enum


class ErrorCode(str, Enum):
    """
    Standard application error codes.

    These codes form the public error contract
    between the backend and frontend.
    """

    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UPLOAD_NOT_FOUND = "UPLOAD_NOT_FOUND"

    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    UNAUTHORIZED = "UNAUTHORIZED"

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"