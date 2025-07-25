from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.infrastructure.database.session import Base, engine
from app.interfaces.api.routers import collect_routers


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Chat Server API",
    version="0.1.0",
    lifespan=lifespan
)

for router in collect_routers():
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)