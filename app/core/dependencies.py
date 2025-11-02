from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.core.config import settings
from app.repositories.user_repo import UserRepository
from app.repositories.token_repo import TokenRepository
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

oauth2_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = token.credentials
    # 로그아웃된(블랙리스트) 토큰인지 확인
    if await TokenRepository.is_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    # JWT 토큰 검증
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 유저 정보 조회
    user = await UserRepository.get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 검증 완료 → 유저 반환
    return user
