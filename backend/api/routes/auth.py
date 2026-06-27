## Auth Routes

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.auth import (UserCreate, UserLogin, TokenResponse)
from services.auth_service import (register_user, authenticate_user)
from api.deps.db import  get_db
from fastapi.security import OAuth2PasswordRequestForm

from api.deps.auth import get_current_user
from schemas.user import UserResponse
from models.user import User

router = APIRouter(
	prefix="/auth",
	tags=["Authentication"]
)

@router.post("/register")
async def register(user_data: UserCreate, db:Session = Depends(get_db)):
	user = register_user(
		db,
		user_data.email,
		user_data.password
	)

	if not user:
		raise HTTPException(
			status_code=400,
			detail="User already exists"
		)
	return {"message":"User created successfulyy"}

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db:Session = Depends(get_db)):
	token = authenticate_user(db, user_data.email, user_data.password)
	if not token:
		raise HTTPException(status_code=401, detail="Invalid credentials")
	return {"access_token": token}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
	return current_user


@router.post(
    "/token",
    response_model=TokenResponse
)
async def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
