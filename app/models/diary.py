from tortoise import fields
from tortoise.models import Model

class Diary(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, null=True)
    content = fields.TextField()

    user = fields.ForeignKeyField(
        "models.User",
        related_name="diaries",
        on_delete="CASCADE",
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "diary"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Diary(id={self.id}, user_id={self.user_id}, title={self.title})"
