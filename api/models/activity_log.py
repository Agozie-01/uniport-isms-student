from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_activities')
    title = models.CharField(max_length=255, default="")    # Title of the activity
    action = models.TextField()  # Detailed description
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of the activity

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        db_table = "activity_logs"  # Explicitly set the table name