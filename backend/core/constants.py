from django.db import models
from django.utils.translation import gettext_lazy as _

class RequestStatus(models.TextChoices):
    DRAFT = 'DRAFT', _('Draft')
    REVIEW = 'REVIEW', _('In Review')
    APPROVED = 'APPROVED', _('Approved')
    COMPLETED = 'COMPLETED', _('Completed')
    ARCHIVED = 'ARCHIVED', _('Archived')

class TaskStatus(models.TextChoices):
    TODO = 'TODO', _('To Do')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    REVIEW = 'REVIEW', _('In Review')
    DONE = 'DONE', _('Done')
    BLOCKED = 'BLOCKED', _('Blocked')
    CANCELLED = 'CANCELLED', _('Cancelled')

class Priority(models.TextChoices):
    LOW = 'LOW', _('Low')
    MEDIUM = 'MEDIUM', _('Medium')
    HIGH = 'HIGH', _('High')
    URGENT = 'URGENT', _('Urgent')