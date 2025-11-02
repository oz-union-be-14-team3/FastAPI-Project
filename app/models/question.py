from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

# F821 error
if TYPE_CHECKING:
    from app.models.user_question import UserQuestion

class Question(Model):
    id = fields.IntField(pk=True)
    question_text = fields.TextField()

    user_questions: fields.ReverseRelation["UserQuestion"]

    class Meta:
        table = "questions"
