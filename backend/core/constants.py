"""
Application-wide constants.

Business logic should import values from here instead of
hardcoding them.
"""

# Upload limits
MAX_UPLOAD_SIZE = 25 * 1024 * 1024  # 25 MB


# Supported MIME types
ALLOWED_UPLOAD_TYPES = {
    "application/pdf",
    "text/plain",
    "text/csv",
}

# Upload directory
UPLOAD_ROOT = "uploads"