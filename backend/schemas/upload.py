from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: UUID
    original_filename: str
    mime_type: str
    file_size: int
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True