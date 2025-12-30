import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from api_v1 import router as router_v1
from core.config import settings
from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title=settings.name,
    description=settings.description,
    version=settings.version,
    lifespan=lifespan,
)

app.include_router(
    router=router_v1,
    prefix=settings.api_v1_prefix,
)

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host=settings.host,
        port=settings.port,
        reload=True if settings.debug else False,
    )
