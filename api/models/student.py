from django.db import models
from .department import Department

class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    matric_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="students")
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active', 
        null=True, 
        blank=True
    ) 

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matric_number})"

    class Meta:
        db_table = "students"  # Explicitly set the table name
