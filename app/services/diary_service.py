from fastapi import HTTPException, status
from app.repositories.diary_repo import DiaryRepository
from app.schemas.diary import DiaryCreate, DiaryUpdate


class DiaryService:
    # ✏️ 글 작성
    @staticmethod
    async def create_diary(user_id: int, data: DiaryCreate):
        diary = await DiaryRepository.create_diary(data.title, data.content, user_id)
        return diary

    # 📚 전체 글 조회
    @staticmethod
    async def get_all_diaries(user_id: int):
        diaries = await DiaryRepository.get_all_by_user(user_id)
        return diaries

    # 🔍 단일 글 조회
    @staticmethod
    async def get_diary_by_id(diary_id: int, user_id: int):
        diary = await DiaryRepository.get_by_id(diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")
        if diary.user_id != user_id:
            raise HTTPException(status_code=403, detail="Permission denied")
        return diary

    # 🛠 글 수정
    @staticmethod
    async def update_diary(diary_id: int, user_id: int, data: DiaryUpdate):
        diary = await DiaryRepository.get_by_id(diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")
        if diary.user_id != user_id:
            raise HTTPException(status_code=403, detail="You are not the author of this diary")

        updated = await DiaryRepository.update_diary(diary, data.title, data.content)
        return updated

    # ❌ 글 삭제
    @staticmethod
    async def delete_diary(diary_id: int, user_id: int):
        diary = await DiaryRepository.get_by_id(diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="Diary not found")

        if diary.user_id != user_id:
            raise HTTPException(status_code=403, detail="You are not the author of this diary")

        await DiaryRepository.delete_diary(diary)
        return {"message": "Diary deleted successfully"}
