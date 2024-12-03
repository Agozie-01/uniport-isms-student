from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .department import Department

class Admin(AbstractUser):
    """
    Custom admin model extending Django's AbstractUser with additional fields.
    """
    is_superadmin = models.BooleanField(default=False)  # Indicates if the user has superuser privileges
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    # Resolve conflicts by defining unique related_name values
    groups = models.ManyToManyField(
        Group,
        related_name="custom_admins_groups",  # Avoid conflict with default User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_admins_permissions",  # Avoid conflict with default User.user_permissions
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = "admins"  # Explicitly set the table name
