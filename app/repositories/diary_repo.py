from app.models.diary import Diary
from app.models.user import User


class DiaryRepository:
    @staticmethod
    async def get_all_diary():
        return await Diary.all()
    
    @staticmethod
    async def create_diary(title:str, content:str, user:User)->Diary:
        return await Diary.create(title=title, content=content, user=user)