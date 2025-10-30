from fastapi import APIRouter,Depends, Request
from fastapi.templating import Jinja2Templates
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from fastapi.security import HTTPAuthorizationCredentials
from app.core.dependencies import oauth2_scheme,get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

template = Jinja2Templates("app/templates")

@router.get("/")
async def read_auth(request: Request):
    return template.TemplateResponse("auth.html", {"request": request})


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await AuthService.register(user.username, user.email, user.password)

@router.post("/login")
async def login(user: UserLogin):
    return await AuthService.login(user.username, user.password)

@router.post("/logout")
async def logout(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    current_user = Depends(get_current_user)
):
    token_str = token.credentials 
    return await AuthService.logout(token_str, current_user)
