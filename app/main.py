from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import healthschecker
from core.fastapi_config import FastAPIConfig

app = FastAPI()

origins = [
    "*"
]
fastapi_settings = FastAPIConfig()

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
