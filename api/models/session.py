from django.db import models
from .semester import Semester  # Assuming Semester model exists

class Session(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "2023/2024"
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="sessions")  # ForeignKey to Semester
    start_date = models.DateField()  # Start date of the session
    end_date = models.DateField()  # End date of the session
    is_active = models.BooleanField(default=True)  # Indicates if the session is active
    created_at = models.DateTimeField(auto_now_add=True)  # When the session was created
    updated_at = models.DateTimeField(auto_now=True)  # When the session was last updated

    def __str__(self):
        return f"{self.name} - {self.semester.name}"

    class Meta:
        db_table = "sessions"
        unique_together = ("name", "semester")  # Prevent duplicate session-semester combinations
