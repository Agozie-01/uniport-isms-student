from django.db import models
from .department import Department

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    credit_hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        db_table = "courses"  # Explicitly set the table name
