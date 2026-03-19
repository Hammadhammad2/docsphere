from django.db import models
from django_extensions.db.models import TimeStampedModel

from organizations.models import Organization


class Project(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
