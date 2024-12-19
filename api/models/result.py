from django.db import models
from .course import Course
from .student import Student
from decimal import Decimal, InvalidOperation

class Result(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('review', 'Under Review'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="results")
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Supports scores like 89.5
    grade = models.CharField(max_length=2)  # e.g., "A", "B", etc.
    gp = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0)  # Grade point (e.g., 4.00)
    qp = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)  # Quality points
    status = models.CharField(
        max_length=10,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',  # Default status when a result is first created
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Tracks when the record is created
    updated_at = models.DateTimeField(auto_now=True)  # Tracks when the record is last updated

    def save(self, *args, **kwargs):
        """
        Automatically calculate and update grade point (gp) and quality points (qp)
        before saving the result record.
        """
        if not self.course:
            raise ValueError("Course cannot be None")
        if self.score is None:
            raise ValueError("Score cannot be None or empty")
        
        try:
            self.score = Decimal(str(self.score))  # Convert score to Decimal
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError(f"Invalid score value: {self.score}. It must be a valid decimal number.")

        if not hasattr(self.course, 'credit_units') or self.course.credit_units is None:
            raise ValueError(f"Course '{self.course}' does not have valid credit_units")

        self.gp = self.calculate_grade_point()
        self.qp = self.gp * self.course.credit_units
        self.grade = self.map_grade(self.gp)
        super(Result, self).save(*args, **kwargs)

    def calculate_grade_point(self):
        """Calculates the grade point based on the score."""
        if self.score is None:
            raise ValueError("Score cannot be None")
        if self.score >= 70:
            return 5  # A
        elif self.score >= 60:
            return 4  # B
        elif self.score >= 50:
            return 3  # C
        elif self.score >= 45:
            return 2  # D
        elif self.score >= 40:
            return 1  # E
        else:
            return 0  # F

    def map_grade(self, grade_point):
        """Maps the grade point to a grade."""
        grade_mapping = {
            5: "A",
            4: "B",
            3: "C",
            2: "D",
            1: "E",
            0: "F",
        }
        return grade_mapping.get(grade_point, "F")

    def __str__(self):
        return f"{self.student} - {self.course} - {self.score} - {self.get_status_display()}"

    class Meta:
        db_table = "results"
        ordering = ['-created_at']  # Order results by creation date, newest first
