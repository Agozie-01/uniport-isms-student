from django.db import models
from .department import Department
from .session import Session

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name="courses")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="courses")  # Link to session
    credit_units = models.IntegerField(default=3)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.session})"

    class Meta:
        db_table = "courses"

