from pydantic import BaseModel

class DiaryCreate(BaseModel):
    title : str
    content : str

class DiaryResponse(BaseModel):
    id : int
    user_id : int
    title : str
    content : str