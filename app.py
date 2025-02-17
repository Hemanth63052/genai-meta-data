from fastapi import FastAPI

app = FastAPI(
    description="This is a GenAI API. This is the initial interaction point with the GenAI API, serving as the first level of communication with the user interface.",
    version="0.1.0",
    title="GenAI API",
    contact={
        "name": "Hemanth Kumar Pasham",
        "url": "https://github.com/Hemanth63052/GenAI-API",
    },
    root_path="/api",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=True,
    )

