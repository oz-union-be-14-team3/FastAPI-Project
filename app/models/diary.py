from tortoise import fields
from tortoise.models import Model


class Diary(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="diaries",
        on_delete=fields.CASCADE, index=True
    )

    class Meta:
        table = "diaries"
