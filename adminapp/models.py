from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    matric_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # New field for login
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.IntegerField(default=100)
    status = models.CharField(max_length=20, default="active")

    def set_password(self, raw_password):
        """Hash password before saving."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if password matches."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    unit = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code}"
