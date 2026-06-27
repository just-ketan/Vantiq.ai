from core.error_codes import ErrorCode


class VantiqException(Exception):
    def __init__(
        self,
        error_code: ErrorCode,
        message: str,
        status_code: int,
    ):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code

        super().__init__(message)

class UploadException(VantiqException):
    pass

class AuthException(VantiqException):
    pass