from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Document(TimeStampedModel):
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, default="")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_documents",
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title
