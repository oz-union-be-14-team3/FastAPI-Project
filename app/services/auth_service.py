from fastapi import HTTPException
from app.repositories.user_repo import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from jose import jwt
from app.repositories.token_repo import TokenRepository
from datetime import datetime
from app.core.config import settings


class AuthService:
    @staticmethod
    async def register(username: str, email: str, password: str):
        if await UserRepository.get_by_username(username):
            raise HTTPException(status_code=400, detail="Username already exists")

        password_hash = get_password_hash(password)
        user = await UserRepository.create_user(username, email, password_hash)
        return user

    @staticmethod
    async def login(username: str, password: str):
        user = await UserRepository.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def logout(token: str, current_user):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            exp = datetime.fromtimestamp(payload["exp"])
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid token")

        await TokenRepository.add(token, current_user.id, exp)
        return {"msg": "Successfully logged out"}
