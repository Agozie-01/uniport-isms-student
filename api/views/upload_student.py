from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pandas as pd

from ..models import Student, Department


class UploadStudentsView(APIView):
    """
    Endpoint to upload or update student records from a spreadsheet.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Process the uploaded file
            df = self.read_file(file)
            if isinstance(df, Response):
                return df  # If read_file returns an error response, return it

            return self.process_students(df)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_file(self, file):
        """Reads the uploaded file and returns a DataFrame or an error response."""
        try:
            df = pd.read_excel(file)
            required_columns = {
                "first_name", "last_name", "matric_number", 
                "email", "date_of_birth", "department_id", 
                "level", "status"
            }
            if not required_columns.issubset(df.columns):
                missing_columns = required_columns - set(df.columns)
                return Response(
                    {"error": f"Missing required columns: {missing_columns}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return df
        except Exception as e:
            return Response({"error": f"Error reading file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def process_students(self, df):
        """Processes the student records from the DataFrame."""
        created_students = []
        updated_students = []
        errors = []

        for _, row in df.iterrows():
            self.process_student_row(row, created_students, updated_students, errors)

        return Response(
            {
                "message": "Processing completed.",
                "created_students": created_students,
                "updated_students": updated_students,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )

    def process_student_row(self, row, created_students, updated_students, errors):
        """Processes a single row of the DataFrame."""
        try:
            department = self.get_department(row["department_id"])
            if isinstance(department, dict):  # If get_department returns an error
                errors.append(department)
                return

            existing_student = Student.objects.filter(matric_number=row["matric_number"]).first()
            if existing_student:
                self.update_student(existing_student, row, department, updated_students, errors)
            else:
                self.create_student(row, department, created_students, errors)

        except Exception as e:
            errors.append(
                {
                    "matric_number": row.get("matric_number"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def get_department(self, department_id):
        """Fetches the department by ID or returns an error."""
        try:
            return Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return {
                "matric_number": None,
                "error": f"Department with ID {department_id} does not exist.",
            }

    def update_student(self, student, row, department, updated_students, errors):
        """Updates an existing student record."""
        if student.email != row["email"] and Student.objects.filter(email=row["email"]).exists():
            errors.append(
                {
                    "matric_number": row["matric_number"],
                    "error": f"Email {row['email']} is already in use.",
                }
            )
            return

        student.first_name = row["first_name"]
        student.last_name = row["last_name"]
        student.email = row["email"]
        student.date_of_birth = row["date_of_birth"]
        student.department = department
        student.level = row["level"]
        student.status = row["status"] or "active"
        student.save()
        updated_students.append(student.matric_number)

    def create_student(self, row, department, created_students, errors):
        """Creates a new student record."""
        if Student.objects.filter(email=row["email"]).exists():
            errors.append(
                {
                    "matric_number": row["matric_number"],
                    "error": f"Email {row['email']} is already in use.",
                }
            )
            return

        Student.objects.create(
            first_name=row["first_name"],
            last_name=row["last_name"],
            matric_number=row["matric_number"],
            email=row["email"],
            date_of_birth=row["date_of_birth"],
            department=department,
            level=row["level"],
            status=row["status"] or "active",
        )
        created_students.append(row["matric_number"])
