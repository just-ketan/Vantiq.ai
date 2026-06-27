from sqlalchemy.orm import Session
from models.document import Document
from models.user import User
from models.upload import Upload
from models.enums import (DocumentStatus, ProcessingStage,)
from ai.pipeline.ingestion_pipeline import IngestionPipeline

class DocumentService:
    def __init__(self):
        self.pipeline = IngestionPipeline()

    def create_document(self, db:Session, upload: Upload, current_user: User) -> Document:
        document = Document(
            upload_id = upload.id,
            user_id = current_user.id,
            filename = upload.original_filename,
            mime_type = upload.mime_type,
            file_size = upload.file_size,
            status = DocumentStatus.UPLOADED.value,
            processing_stage = ProcessingStage.UPLOAD.value
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def get_document(self, db:Session, document_id, current_user: User):
        return (
            db.query(Document)
            .filter(Document.id == document_id, Document.user_id == current_user.id)
            .first()
        )

    def update_status(self, db:Session, document: Document, *, status=None, stage=None, srror_message=None):
        if status:
            document.status = status
        if stage:
            document.stage = stage
        if error_message:
            document.error_message = error_message

        db.commit()
        db.refresh(document)
        return document

    def extract_document(self, db:Session, document: Document):
        extraction = self.pipeline.extract_document(document)
        return extraction