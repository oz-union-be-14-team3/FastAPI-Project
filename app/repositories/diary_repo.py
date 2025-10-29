from app.models.diary import Diary
from app.schemas.diary_schema import DiaryCreate, DiaryUpdate

# ✅ Create
async def create_diary(data: DiaryCreate, user_id: int):
    diary = await Diary.create(**data.dict(), user_id=user_id)
    return diary

# ✅ Read All
async def get_all_diaries():
    return await Diary.all().prefetch_related("user")

# ✅ Read One
async def get_diary_by_id(diary_id: int):
    return await Diary.get_or_none(id=diary_id)

# ✅ Update
async def update_diary(diary_id: int, data: DiaryUpdate):
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        return None
    updated_data = data.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(diary, key, value)
    await diary.save()
    return diary

# ✅ Delete
async def delete_diary(diary_id: int):
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        return None
    await diary.delete()
    return diary
