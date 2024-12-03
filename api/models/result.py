from django.db import models
from .course import Course
from .student import Student

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="results")
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Supports scores like 89.5
    grade = models.CharField(max_length=2)  # e.g., "A", "B", etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.score}"

    class Meta:
        db_table = "results"  # Explicitly set the table name