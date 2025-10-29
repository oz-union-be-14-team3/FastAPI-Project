from fastapi import APIRouter, HTTPException
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryOut
from app.repositories import diary_repo

router = APIRouter(prefix="/diaries", tags=["Diary CRUD"])

# ✅ 전체 조회
@router.get("/", response_model=list[DiaryOut])
async def list_diaries():
    diaries = await diary_repo.get_all_diaries()
    return diaries

# ✅ 단일 조회
@router.get("/{diary_id}", response_model=DiaryOut)
async def get_diary(diary_id: int):
    diary = await diary_repo.get_diary_by_id(diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary

# ✅ 생성
@router.post("/", response_model=DiaryOut)
async def create_diary(diary: DiaryCreate):
    new_diary = await diary_repo.create_diary(diary, user_id=1)  # TODO: 실제 로그인 유저 ID 적용 필요
    return new_diary

# ✅ 수정
@router.put("/{diary_id}", response_model=DiaryOut)
async def update_diary(diary_id: int, diary_data: DiaryUpdate):
    updated = await diary_repo.update_diary(diary_id, diary_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Diary not found")
    return updated

# ✅ 삭제
@router.delete("/{diary_id}")
async def delete_diary(diary_id: int):
    deleted = await diary_repo.delete_diary(diary_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Diary not found")
    return {"message": "Diary deleted successfully"}
