from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.conf import settings
from core.models import SoftDeleteModel, Organization
from clients.models import Client
from core.constants import RequestStatus, Priority

class ServiceRequest(SoftDeleteModel):
    """
    The core unit of work in PSMS.
    Tracks a request from DRAFT -> ARCHIVED.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Ownership
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='service_requests')
    
    # Roles [cite: 205, 206]
    # The 'manager' approves the work
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='managed_requests'
    )
    # The 'lead_consultant' does the work
    lead_consultant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='led_requests'
    )

    # Core Data [cite: 208-212]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=RequestStatus.choices, 
        default=RequestStatus.DRAFT
    )
    priority = models.CharField(
        max_length=20, 
        choices=Priority.choices, 
        default=Priority.MEDIUM
    )
    due_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps [cite: 214]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # deleted_at is handled by SoftDeleteModel

    def __str__(self):
        return f"{self.title} ({self.status})"