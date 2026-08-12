from fastapi import FastAPI

from shared_kernel.infra.container import AppContainer
from shared_kernel.infra.database.orm import init_orm_mappers

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
    return {"ping": "pong"}