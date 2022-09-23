from xml.etree.ElementTree import PI

from django.db import models
from django.utils.translation import gettext_lazy as _


class PipelineTypes(models.TextChoices):
    IMPORT = "I", _("Import")
    REIMPORT = "R", _("Reimport")


class TaskStatus(models.TextChoices):
    RUNNING = "R", _("Running")
    SUCCESS = "S", _("Success")
    FAILURE = "F", _("Failure")


class Task(models.Model):
    celery_task_id = models.CharField(max_length=36)
    name = models.CharField(max_length=255)
    started_on = models.DateTimeField(auto_now_add=True)
    pipeline_type = models.CharField(
        max_length=1, choices=PipelineTypes.choices, default=PipelineTypes.IMPORT
    )
    pipeline_config = models.JSONField()
    status = models.CharField(
        max_length=1, choices=TaskStatus.choices, default=TaskStatus.RUNNING
    )
    completed_on = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=32, null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def is_completed(self):
        return self.status == TaskStatus.SUCCESS or self.status == TaskStatus.FAILURE
