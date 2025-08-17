from fastapi import FastAPI
from contextlib import asynccontextmanager
from common.database.db_connection import Base, engine
from producer.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Image To Text - API",description="API service for uploading images, creating OCR jobs, "
                "tracking job status, and retrieving results.", lifespan=lifespan)

app.include_router(api_router)
