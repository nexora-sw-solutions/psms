import uuid
from django.db import models
from core.models import SoftDeleteModel, Organization

class Client(SoftDeleteModel):
    """
    Stub model for Phase 2. 
    The Other Developer will add fields like industry, status, etc. later.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    # Placeholder for future fields
    
    def __str__(self):
        return self.name