from django.db import models


class Role(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"


class InviteStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    EXPIRED = "expired", "Expired"
