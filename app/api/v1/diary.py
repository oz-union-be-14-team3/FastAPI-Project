from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryOut
from app.repositories.diary_repo import DiaryRepository
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/diaries", tags=["Diary CRUD"])


# ✅ [1] 내 모든 일기 조회
@router.get("/", response_model=list[DiaryOut])
async def list_diaries(current_user: User = Depends(get_current_user)):
    diaries = await DiaryRepository.get_all_diaries_by_user(current_user.id)
    return diaries


# ✅ [2] 단일 일기 조회
@router.get("/{diary_id}", response_model=DiaryOut)
async def get_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await DiaryRepository.get_diary_by_id(diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return diary


# ✅ [3] 일기 생성 (자동으로 user 연결)
@router.post("/", response_model=DiaryOut, status_code=status.HTTP_201_CREATED)
async def create_diary(
    diary_data: DiaryCreate,
    current_user: User = Depends(get_current_user)
):
    new_diary = await DiaryRepository.create_diary(
        title=diary_data.title,
        content=diary_data.content,
        user=current_user 
    )
    return new_diary


# ✅ [4] 일기 수정 (작성자 본인만)
@router.put("/{diary_id}", response_model=DiaryOut)
async def update_diary(
    diary_id: int,
    diary_data: DiaryUpdate,
    current_user: User = Depends(get_current_user)
):
    diary = await DiaryRepository.get_diary_by_id(diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    updated_diary = await DiaryRepository.update_diary(diary_id, diary_data)
    return updated_diary


# ✅ [5] 일기 삭제 (작성자 본인만)
@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await DiaryRepository.get_diary_by_id(diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    await DiaryRepository.delete_diary(diary_id)
    return {"message": "Diary deleted successfully"}
