from django.db import models
from django.db.models.fields import uuid

from config.models import TimestampModel

from .choices import InviteStatus, Role


class Organization(TimestampModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Membership(TimestampModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"], name="unique_user_organization"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"


class Invite(TimestampModel):
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="invites")
    invited_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="invites")
    status = models.CharField(max_length=255, choices=InviteStatus.choices, default=InviteStatus.PENDING)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.email} - {self.organization} ({self.status})"
