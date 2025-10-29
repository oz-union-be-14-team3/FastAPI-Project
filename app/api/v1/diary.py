from fastapi import APIRouter, Depends, HTTPException
from app.models.diary import Diary
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/diary", tags=["Diary"])

@router.put("/{diary_id}")
async def update_diary(
    diary_id: int,
    title: str,
    content: str,
    current_user: User = Depends(get_current_user)
):
    # 글 존재 여부 확인
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    # 권한 체크: 본인 글인지 확인
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the author of this diary")

    # 수정
    diary.title = title
    diary.content = content
    await diary.save()

    return {"message": "Diary updated successfully", "diary": diary}

@router.delete("/{diary_id}")
async def delete_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user)
):
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the author of this diary")

    await diary.delete()
    return {"message": "Diary deleted successfully"}
