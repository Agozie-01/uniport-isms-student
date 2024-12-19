from django.db import models

class Session(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "2023/2024"
    start_date = models.DateField()  # Start date of the session
    end_date = models.DateField()  # End date of the session
    is_active = models.BooleanField(default=True)  # Indicates if the session is active
    created_at = models.DateTimeField(auto_now_add=True)  # When the session was created
    updated_at = models.DateTimeField(auto_now=True)  # When the session was last updated

    def __str__(self):
        return f"{self.name}"  # Corrected to display only the session name

    class Meta:
        db_table = "sessions"
