from fastapi import FastAPI
from sqlmodel import SQLModel

from routers import create, user
from reviews import review
from db import engine

from pages.router import router as router_pages
app = FastAPI()
app.include_router(user.router)
app.include_router(create.router)
app.include_router(review.router)
app.include_router(router_pages)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем шаблоны
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Определение маршрутов для HTML страниц
@app.get("/", response_class=HTMLResponse)
async def root():
    return templates.TemplateResponse("login.html", {"request": {}})

@app.get("/register/", response_class=HTMLResponse)
async def register_page():
    return templates.TemplateResponse("register.html", {"request": {}})

@app.get("/change_password/", response_class=HTMLResponse)
async def change_password_page():
    return templates.TemplateResponse("change_password.html", {"request": {}})

@app.get("/update/", response_class=HTMLResponse)
async def update_page():
    return templates.TemplateResponse("update_user.html", {"request": {}})





# # If you have any startup/shutdown events
# @app.on_event("startup")
# async def startup_event():
#     # Startup logic here
#     pass
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     # Shutdown logic here
#     pass


SQLModel.metadata.create_all(engine)