from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps.auth import get_current_user
from api.deps.db import get_db

from models.document import Document
from models.user import User

from services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"],)

document_service = DocumentService()
#     # temp route to check document extraction
@router.post("/{document_id}/extract")
def extract_document(document_id: UUID, db:Session = Depends(get_db), current_user:User = Depends(get_current_user),):
    document = document_service.get_document(db=db, document_id=document_id, current_user=current_user,)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document_service.extract_document(db=db, document=document)
