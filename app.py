from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from scripts import all_routers

app = FastAPI(
    description="This is a GenAI API. This is the initial interaction point with the GenAI API, serving as the first level of communication with the user interface.",
    version="0.1.0",
    title="GenAI API",
    contact={
        "name": "Hemanth Kumar Pasham",
        "url": "https://github.com/Hemanth63052/genai-meta-data",
    },
    root_path="/api",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=True,
    )

app.include_router(router=all_routers)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
