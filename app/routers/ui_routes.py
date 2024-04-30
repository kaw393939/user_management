from builtins import dict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates

from app import routers
from app.dependencies import get_current_user, get_settings

router = APIRouter()
settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request, current_user: dict = Depends(get_current_user, use_cache=False)):
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})

@router.get("/register-form", include_in_schema=False)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login-form", include_in_schema=False)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/dashboard", include_in_schema=False)
async def dashboard(request: Request, current_user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})