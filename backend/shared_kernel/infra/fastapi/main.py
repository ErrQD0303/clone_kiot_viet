"""FastAPI application entry point"""
from logging import getLogger

from fastapi import FastAPI

from shared_kernel.infra.database.orm import init_orm_mappers
from shared_kernel.infra.container import AppContainer
from shared_kernel.infra.logging import configure_logging

configure_logging()

logger = getLogger(__name__)

app_container = AppContainer()

app = FastAPI(
    title="Clone KiotViet",
    contact={
        "name": "ERRQD0303",
        "email": "quocdat3396@gmail.com"
    }
)

app.container = app_container
# app.include_router(reception_api.router)

init_orm_mappers()

@app.get("/")
def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    return "ok"
