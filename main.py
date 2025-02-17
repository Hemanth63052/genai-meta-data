import uvicorn
from scripts.config import ServerConfig
from scripts.logging import logger
from app import app as fastapi_app

if __name__ == "__main__":
    logger.info(f"Starting server at {ServerConfig.SERVER_HOST}:{ServerConfig.SERVER_PORT}")
    uvicorn.run(
        app=fastapi_app,
        host=ServerConfig.SERVER_HOST,
        port=ServerConfig.SERVER_PORT,
    )
