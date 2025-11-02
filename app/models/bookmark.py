from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.models import Model

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.quote import Quote


class Bookmark(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="bookmarks",
        on_delete=fields.CASCADE, index=True
    )
    quote = fields.ForeignKeyField(
        "models.Quote",
        related_name="bookmarks",
        on_delete=fields.CASCADE, index=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "bookmarks"
