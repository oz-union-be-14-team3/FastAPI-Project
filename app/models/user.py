from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True)
    password_hash = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    diaries: fields.ReverseRelation["Diary"]
    bookmarks: fields.ReverseRelation["Bookmark"]
    user_questions: fields.ReverseRelation["UserQuestion"]
    token_blacklists: fields.ReverseRelation["TokenBlacklist"]

    class Meta:
        table = "users"
