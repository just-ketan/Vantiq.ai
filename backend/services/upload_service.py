import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from models.enums import UploadStatus
from models.upload import Upload
from models.user import User
from storage.factory import get_storage
from core.logger import logger
from core.constants import (ALLOWED_UPLOAD_TYPES, MAX_UPLOAD_SIZE,)
from http import HTTPStatus
from core.exceptions import UploadException
from core.error_codes import ErrorCode
from fastapi import UploadFile
from services.document_service import DocumentService

class UploadService:

    def __init__(self):
        self.storage = get_storage()
        self.document_service = DocumentService()

    async def upload_file(
        self,
        db: Session,
        current_user: User,
        file: UploadFile,
    ) -> Upload:

        # ---------- Read file ----------
        content = await file.read()
        # ---------- Validate MIME type ----------
        self._validate_file_type(file)
        # ---------- Validate size ----------
        self._validate_file_size(content)

        # ---------- Generate unique filename ----------
        stored_filename = self._generate_filename(file.filename)
        # ---------- Store file ----------
        storage_path = self._save_to_storage(current_user,stored_filename,content,)

        # ---------- Save metadata ----------
        upload = self._build_upload(
            current_user,
            file,
            stored_filename,
            storage_path,
            len(content),
        )

        db.add(upload)
        db.commit()
        db.refresh(upload)
        self.document_service.create_document(
            db=db,
            upload=upload,
            current_user=current_user,
        )

        logger.info(
            "User %s uploaded %s (%d bytes)",
            current_user.email,
            file.filename,
            len(content),
        )

        return upload

    def list_uploads(
        self,
        db: Session,
        current_user: User,
    ):
        return (
            db.query(Upload)
            .filter(Upload.user_id == current_user.id)
            .order_by(Upload.uploaded_at.desc())
            .all()
        )

    def delete_upload(
        self,
        db: Session,
        current_user: User,
        upload_id,
    ):

        upload = (
            db.query(Upload)
            .filter(
                Upload.id == upload_id,
                Upload.user_id == current_user.id,
            )
            .first()
        )

        if upload is None:
            raise UploadException(
                ErrorCode.UPLOAD_NOT_FOUND,
                "Upload not found",
            )

        self.storage.delete_file(upload.storage_path)

        db.delete(upload)
        db.commit()
        logger.info(
            "User %s deleted upload %s",
            current_user.email,
            upload.id,
        )

# ------------------- private helpers ---------------------
    def _validate_file_type(
        self,
        file: UploadFile,
    ) -> None:

        if file.content_type not in ALLOWED_UPLOAD_TYPES:
            logger.warning(
                "Rejected upload '%s' with unsupported MIME type '%s'",
                file.filename,
                file.content_type,
            )
            raise UploadException(
                ErrorCode.INVALID_FILE_TYPE,
                "Unsupported file type",
            )
                
    def _validate_file_size(
        self,
        content: bytes,
    ) -> None:

        if len(content) > MAX_UPLOAD_SIZE:
            logger.warning(
                "Rejected upload because file size exceeded limit (%d bytes)",
                len(content),
            )
            raise UploadException(
                ErrorCode.FILE_TOO_LARGE,
                "File exceeds maximum upload size",
            )
    
    def _generate_filename(
        self,
        original_filename: str,
    ) -> str:
        """
        Generate a unique filename while preserving
        the original file extension.
        """
        extension = Path(original_filename).suffix.lower()
        return f"{uuid.uuid4()}{extension}"

    def _save_to_storage(
        self,
        current_user: User,
        stored_filename: str,
        content: bytes,
    ) -> str:
        """
        Save the file using the configured
        storage provider.
        """
        return self.storage.save_file(current_user.id,stored_filename,content,)

    def _build_upload(
        self,
        current_user: User,
        file: UploadFile,
        stored_filename: str,
        storage_path: str,
        file_size: int,
    ) -> Upload:
        """
        Build an Upload entity from the supplied metadata.
        """
        return Upload(
            user_id=current_user.id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=file.content_type,
            file_size=file_size,
            storage_path=storage_path,
            status=UploadStatus.UPLOADED.value,
        )