import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# 1. The Utilities 
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()  # Default manager
    all_objects = models.Manager() # Access to deleted items if needed

    class Meta:
        abstract = True 

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

# 2. Organization 
class Organization(SoftDeleteModel): 
    """
    Foundation for multi-tenancy.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 3. User Manager 
class UserManager(BaseUserManager):
    """Custom manager that respects soft deletes."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'SUPER_ADMIN')
        return self.create_user(email, password, **extra_fields)

# 4. User Model 
class User(SoftDeleteModel, AbstractUser):
    """
    Custom User model with UUID, Roles, and Organization link.
    """
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
        FIRM_ADMIN = 'FIRM_ADMIN', _('Firm Admin')
        MANAGER = 'MANAGER', _('Manager')
        CONSULTANT = 'CONSULTANT', _('Consultant')
        CLIENT = 'CLIENT', _('Client')

    username = None 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    
    # Relationships
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )
    
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.CONSULTANT
    )
    
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # deleted_at is inherited from SoftDeleteModel

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Explicitly set the custom manager
    objects = UserManager() 
    all_objects = models.Manager() # Explicitly add back raw access

    def __str__(self):
        return self.email