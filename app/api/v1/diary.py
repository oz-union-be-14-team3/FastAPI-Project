from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from app.models.diary import Diary

router = APIRouter(prefix="/diary", tags=["Diary"])

@router.put("/{diary_id}")
async def update_diary(diary_id: int, content: str, current_user=Depends(get_current_user)):
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    diary.content = content
    await diary.save()
    return {"message": "Updated successfully"}

