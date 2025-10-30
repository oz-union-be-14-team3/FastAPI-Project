from fastapi import APIRouter,Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from fastapi.security import HTTPAuthorizationCredentials
from app.core.dependencies import oauth2_scheme,get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])




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
