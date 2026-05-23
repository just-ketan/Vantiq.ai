## Auth Routes

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.auth import (UserCreate, UserLogin, TokenResponse)
from services.auth_service import (register_user, authenticate_user)
from api.deps.db import  get_db

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
