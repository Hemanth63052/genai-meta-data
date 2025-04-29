import uvicorn

from dotenv import load_dotenv

load_dotenv()
from adapt_iq_common.config import ServerConfig
from adapt_iq_common.logging import logger
from app import app as fastapi_app

if __name__ == "__main__":
    logger.info(f"Starting server at {ServerConfig.SERVER_HOST}:{ServerConfig.SERVER_PORT}")
    uvicorn.run(
        app=fastapi_app,
        host=ServerConfig.SERVER_HOST,
        port=ServerConfig.SERVER_PORT,
    )
