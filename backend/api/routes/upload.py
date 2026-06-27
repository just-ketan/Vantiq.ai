from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from api.deps.auth import get_current_user
from api.deps.db import get_db

from models.user import User
from schemas.upload import UploadResponse
from services.upload_service import UploadService

from fastapi import HTTPException

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)

service = UploadService()


@router.post("",response_model=UploadResponse,)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.upload_file(
            db,
            current_user,
            file,
    )

@router.get(
    "",
    response_model=list[UploadResponse],
)
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.list_uploads(
        db,
        current_user,
    )


@router.delete("/{upload_id}")
def delete_document(
    upload_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete_upload(
        db,
        current_user,
        upload_id,
    )
    return {
        "message": "Upload deleted successfully"
    }