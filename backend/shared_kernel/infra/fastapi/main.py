"""FastAPI application entry point"""
from logging import getLogger

from fastapi import FastAPI

from identity.presentation.rest.api import identity_router, user_router

from shared_kernel.infra.database.orm import init_orm_mappers
from bootstrap.container import AppContainer
from shared_kernel.infra.fastapi.load_plugins import load_plugins
from shared_kernel.infra.logging import configure_logging

load_plugins()
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
app.container.install_fastapi(app=app)

init_orm_mappers()

@app.get("/")
def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    return "ok"
