from fastapi import APIRouter,Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.core.dependencies import oauth2_scheme,get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await AuthService.register(user.username, user.email, user.password)

@router.post("/login")
async def login(user: UserLogin):
    return await AuthService.login(user.username, user.password)

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user = Depends(get_current_user)
):
    return await AuthService.logout(token, current_user)

