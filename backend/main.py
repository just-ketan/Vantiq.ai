## FastAPI APP boot

from fastapi import FastAPI
from db.session import engine, Base

from api.routes.auth import router as auth_router
from api.routes.upload import router as upload_router
from core.exception_handlers import register_exception_handlers

app = FastAPI(title="vantiq.ai",version="1.0.0")
API_PREFIX = "/api/v1"

register_exception_handlers(app)

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(upload_router, prefix=API_PREFIX)
#Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
	return{
		"message":"vantiq.ai's backend is up and running"
	}

