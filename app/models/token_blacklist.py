from tortoise import fields, models
from app.models.user import User

class TokenBlacklist(models.Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=255, unique=True)
    user = fields.ForeignKeyField("models.User", related_name="blacklisted_tokens")
    expired_at = fields.DatetimeField()

    class Meta:
        table = "token_blacklist"


    def __str__(self):
        return f"TokenBlacklist(user={self.user.username}, token={self.token[:10]}...)"
