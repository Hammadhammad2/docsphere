from django.db import models
from django.db.models.fields import uuid
from django.utils import timezone

from config.models import TimestampModel

from .choices import InviteStatus, Role

INVITE_EXPIRY_DAYS = 7


class Organization(TimestampModel):
    description = models.TextField(blank=True, default="")
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Membership(TimestampModel):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="memberships")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "organization"], name="unique_user_organization")]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"


class Invite(TimestampModel):
    email = models.EmailField()
    expires_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=InviteStatus.choices, default=InviteStatus.PENDING)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    invited_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="invites")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="invites")

    def __str__(self):
        return f"{self.email} - {self.organization} ({self.status})"
