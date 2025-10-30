from fastapi import APIRouter, Depends, status
from typing import List
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.services.diary_service import DiaryService

router = APIRouter(prefix="/diary", tags=["Diary"])


# ✏️ 글 작성
@router.post("/", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(
    data: DiaryCreate,
    current_user: User = Depends(get_current_user)
):
    diary = await DiaryService.create_diary(current_user.id, data)
    return diary


# 📚 전체 글 조회 (내 글만)
@router.get("/", response_model=List[DiaryResponse])
async def get_all_diaries(current_user: User = Depends(get_current_user)):
    diaries = await DiaryService.get_all_diaries(current_user.id)
    return diaries


# 🔍 단일 글 조회
@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user)
):
    diary = await DiaryService.get_diary_by_id(diary_id, current_user.id)
    return diary


# 🛠 글 수정
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    data: DiaryUpdate,
    current_user: User = Depends(get_current_user)
):
    updated = await DiaryService.update_diary(diary_id, current_user.id, data)
    return updated


# ❌ 글 삭제
@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user)
):
    return await DiaryService.delete_diary(diary_id, current_user.id)
