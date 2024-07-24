from fastapi import FastAPI
from sqlmodel import SQLModel

from routers import create, user
from reviews import review
from db import engine

from pages.router import router as router_routers

app = FastAPI()
app.include_router(user.router)
app.include_router(create.router)
app.include_router(review.router)
app.include_router(router_routers)


SQLModel.metadata.create_all(engine)