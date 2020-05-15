from django.db import models


# Create your models here.
from django.db.models.fields import Field

from .constants import ContentType


class ManifestoItem(models.Model):
    title: Field = models.CharField(max_length=500, blank=False)
    description: Field = models.CharField(max_length=5000, blank=True, default="")
    content_type: Field = models.CharField(
        max_length=25,
        choices=[(item.name, item.value) for item in ContentType],
        default=ContentType.VALUE.value,
    )
    owner: Field = models.ForeignKey(
        "auth.User", related_name="items", on_delete=models.CASCADE
    )
