from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

# F821 error
if TYPE_CHECKING:
    from app.models.bookmark import Bookmark

class Quote(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()  # unique=True
    author = fields.CharField(max_length=100, null=True)

    bookmarks: fields.ReverseRelation["Bookmark"]

    class Meta:
        table = "quotes"
