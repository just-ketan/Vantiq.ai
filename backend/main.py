## FastAPI APP boot

from fastapi import FastAPI
from db.session import engine, Base

from api.routes.auth import router as auth_router

app = FastAPI(
	title="vantiq.ai",
	version="1.0.0"
)

app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
	return{
		"message":"vantiq.ai's backend is up and running"
	}

