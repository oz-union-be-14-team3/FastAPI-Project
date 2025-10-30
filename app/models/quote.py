from tortoise import fields
from tortoise.models import Model


class Quote(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()  # unique=True
    author = fields.CharField(max_length=100, null=True)

    bookmarks: fields.ReverseRelation["Bookmark"]

    class Meta:
        table = "quotes"
