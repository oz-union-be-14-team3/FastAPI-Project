from typing import List, Optional
from app.models.diary import Diary


class DiaryRepository:
    # ✏️ 글 작성
    @staticmethod
    async def create_diary(title: Optional[str], content: str, user_id: int) -> Diary:
        return await Diary.create(title=title, content=content, user_id=user_id)

    # 📚 전체 글 조회
    @staticmethod
    async def get_all_by_user(user_id: int) -> List[Diary]:
        return await Diary.filter(user_id=user_id).all()

    # 🔍 단일 글 조회
    @staticmethod
    async def get_by_id(diary_id: int) -> Optional[Diary]:
        return await Diary.get_or_none(id=diary_id)

    # 🛠 글 수정
    @staticmethod
    async def update_diary(diary: Diary, title: Optional[str], content: Optional[str]) -> Diary:
        if title is not None:
            diary.title = title
        if content is not None:
            diary.content = content
        await diary.save()
        return diary

    # ❌ 글 삭제
    @staticmethod
    async def delete_diary(diary: Diary) -> None:
        await diary.delete()
