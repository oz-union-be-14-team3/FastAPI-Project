from fastapi import APIRouter,Depends, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from fastapi.security import HTTPAuthorizationCredentials
from app.core.dependencies import oauth2_scheme,get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth", tags=["Auth"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, summary="다이어리 로그인 페이지")
async def read_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/register", response_model=UserResponse, summary="회원가입")
async def register(user: UserCreate):
    return await AuthService.register(user.username, user.email, user.password)

@router.post("/login", summary="로그인")
async def login(user: UserLogin):
    return await AuthService.login(user.username, user.password)

@router.post("/logout", summary="로그아웃")
async def logout(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    current_user = Depends(get_current_user)
):
    token_str = token.credentials 
    return await AuthService.logout(token_str, current_user)
