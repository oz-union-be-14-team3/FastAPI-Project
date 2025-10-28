from datetime import datetime
from app.models.token_blacklist import TokenBlacklist
from tortoise.exceptions import IntegrityError

class TokenRepository:
    @staticmethod
    async def add(token: str, user_id: int, expired_at: datetime):
        try:
            await TokenBlacklist.create(token=token, user_id=user_id, expired_at=expired_at)
        except IntegrityError:
            pass

    @staticmethod
    async def is_blacklisted(token: str) -> bool:
        return await TokenBlacklist.exists(token=token)
