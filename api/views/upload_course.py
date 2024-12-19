from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pandas as pd
from rest_framework.parsers import MultiPartParser
from ..models import Course, Semester  # Removed import for Session


class UploadCoursesView(APIView):
    """
    Endpoint to upload or update course records from a spreadsheet.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Process the uploaded file
            df = self.read_file(file)
            if isinstance(df, Response):
                return df  # If read_file returns an error response, return it

            return self.process_courses(df)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_file(self, file):
        """Reads the uploaded file and returns a DataFrame or an error response."""
        try:
            df = pd.read_excel(file)
            required_columns = {
                "name", "code", "semester", "credit_units", "description", "is_active"  # Removed 'session' from required columns
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

    def process_courses(self, df):
        """Processes the course records from the DataFrame."""
        created_courses = []
        updated_courses = []
        errors = []

        for _, row in df.iterrows():
            self.process_course_row(row, created_courses, updated_courses, errors)

        return Response(
            {
                "message": "Processing completed.",
                "created_courses": created_courses,
                "updated_courses": updated_courses,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )

    def process_course_row(self, row, created_courses, updated_courses, errors):
        """Processes a single row of the DataFrame."""
        try:
            semester = self.get_semester(row["semester"])  # Now using semester name only
            if isinstance(semester, dict):  # If get_semester returns an error
                errors.append(semester)
                return

            existing_course = Course.objects.filter(code=row["code"]).first()
            if existing_course:
                self.update_course(existing_course, row, semester, updated_courses, errors)
            else:
                self.create_course(row, semester, created_courses, errors)

        except Exception as e:
            errors.append(
                {
                    "code": row.get("code"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def get_semester(self, semester_name):
        """Fetches the semester by name or returns an error."""
        try:
            return Semester.objects.get(name=semester_name)
        except Semester.DoesNotExist:
            return {
                "code": None,
                "error": f"Semester with name '{semester_name}' does not exist.",
            }

    def update_course(self, course, row, semester, updated_courses, errors):
        """Updates an existing course record."""
        course.name = row["name"]
        course.semester = semester  # Now only updating semester
        course.credit_units = row["credit_units"]
        course.description = row["description"]
        course.is_active = row["is_active"]
        course.save()
        updated_courses.append(course.code)

    def create_course(self, row, semester, created_courses, errors):
        """Creates a new course record."""
        Course.objects.create(
            name=row["name"],
            code=row["code"],
            semester=semester,  # Only associating with semester
            credit_units=row["credit_units"],
            description=row["description"],
            is_active=row["is_active"],
        )
        created_courses.append(row["code"])
