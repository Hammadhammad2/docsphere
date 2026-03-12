import uuid

from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from .choices import InviteStatus, Role

INVITE_EXPIRY_DAYS = 7


class Organization(TimeStampedModel):
    description = models.TextField(blank=True, default='')
    name = models.CharField(max_length=255, unique=True)

    members = models.ManyToManyField(
        'users.User', through='organizations.UserOrganization', related_name='organizations'
    )

    def __str__(self):
        return self.name


class UserOrganization(TimeStampedModel):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    organization = models.ForeignKey(
        'organizations.Organization', on_delete=models.CASCADE, related_name='user_organizations'
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_organizations')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'organization'], name='unique_user_organization')]

    def __str__(self):
        return f'{self.user} - {self.organization} ({self.role})'


class Invite(TimeStampedModel):
    email = models.EmailField()
    expires_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=InviteStatus.choices, default=InviteStatus.PENDING)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    invited_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='invites')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='invites')

    def __str__(self):
        return f'{self.email} - {self.organization} ({self.status})'
