from app.models.user import User


class UserRepository:
    @staticmethod
    async def create_user(username: str, email: str, password_hash: str):
        return await User.create(username=username, email=email, password_hash=password_hash)

    @staticmethod
    async def get_by_username(username: str):
        return await User.get_or_none(username=username)
