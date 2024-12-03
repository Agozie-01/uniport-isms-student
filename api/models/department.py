from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g., "CSE" for Computer Science
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "departments"  # Explicitly set the table name
