from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.question import Question


class UserQuestion(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField(
        "models.User",
        related_name="user_questions",
        on_delete=fields.CASCADE, index=True
    )
    question = fields.ForeignKeyField(
        "models.Question",
        related_name="user_questions",
        on_delete=fields.CASCADE, index=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_questions"
        unique_together = (("user", "question", "created_at"),)
