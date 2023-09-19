import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import healthschecker
from app.core.config import FastAPIConfig, origins

fastapi_settings = FastAPIConfig()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthschecker.router)


if __name__ == "__main__":
    uvicorn.run('main:app', host=fastapi_settings.host, port=fastapi_settings.port, reload=fastapi_settings.reload)
