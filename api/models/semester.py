from django.db import models

class Semester(models.Model):
    TERM_CHOICES = [
        ("First Semester", "First Semester"),
        ("Second Semester", "Second Semester"),
        ("Summer Semester", "Summer Semester"),
    ]

    name = models.CharField(max_length=50, unique=True)  # e.g., "First Semester"
    description = models.TextField(blank=True, null=True)  # Optional field for additional info
    start_date = models.DateField()  # The start date of the semester
    end_date = models.DateField()  # The end date of the semester
    is_active = models.BooleanField(default=True)  # If the semester is currently active

    def __str__(self):
        return self.name

    class Meta:
        db_table = "semesters"
