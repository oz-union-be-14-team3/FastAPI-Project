from tortoise import fields
from tortoise.models import Model


class Question(Model):
    id = fields.IntField(pk=True)
    question_text = fields.TextField()

    user_questions: fields.ReverseRelation["UserQuestion"]

    class Meta:
        table = "questions"

