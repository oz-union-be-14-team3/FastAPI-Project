from app.models.diary import Diary
from app.models.user import User
from app.schemas.diary import DiaryUpdate


class DiaryRepository:
    @staticmethod
    async def get_all_diaries_by_user(user_id: int):
        return await Diary.filter(user_id=user_id).all()

    @staticmethod
    async def get_diary_by_id(diary_id: int):
        return await Diary.get_or_none(id=diary_id)

    @staticmethod
    async def create_diary(title: str, content: str, user: User):
        return await Diary.create(title=title, content=content, user=user)

    @staticmethod
    async def update_diary(diary_id: int, diary_data: DiaryUpdate):
        diary = await Diary.get_or_none(id=diary_id)
        if not diary:
            return None
        diary.title = diary_data.title or diary.title
        diary.content = diary_data.content or diary.content
        await diary.save()
        return diary

    @staticmethod
    async def delete_diary(diary_id: int):
        diary = await Diary.get_or_none(id=diary_id)
        if not diary:
            return False
        await diary.delete()
        return True
