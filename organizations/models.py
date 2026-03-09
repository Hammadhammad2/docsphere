from django.conf import settings
from django.db import models
from django.db.models.fields import uuid


class Role(models.TextChoices):
    ADMIN = "admin"
    MEMBER = "member"


class InviteStatus(models.TextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organizations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"], name="unique_user_organization"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"


class Invite(models.Model):
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="invites")
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invites")
    status = models.CharField(max_length=255, choices=InviteStatus.choices, default=InviteStatus.PENDING)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.organization} ({self.status})"
