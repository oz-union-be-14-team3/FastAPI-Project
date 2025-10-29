from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class TokenBlacklist(Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=255)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="token_blacklists",
        on_delete=fields.CASCADE, index=True
    )
    expired_at = fields.DatetimeField(null=True)

    class Meta:
        table = "token_blacklist"
