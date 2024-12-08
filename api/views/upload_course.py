from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pandas as pd
from rest_framework.parsers import MultiPartParser
from ..models import Course, Department, Session


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
                "name", "code", "department_id", "session_id", "credit_units", "description", "is_active"
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
            department = self.get_department(row["department_id"])
            session = self.get_session(row["session_id"])
            if isinstance(department, dict):  # If get_department returns an error
                errors.append(department)
                return
            if isinstance(session, dict):  # If get_session returns an error
                errors.append(session)
                return

            existing_course = Course.objects.filter(code=row["code"]).first()
            if existing_course:
                self.update_course(existing_course, row, department, session, updated_courses, errors)
            else:
                self.create_course(row, department, session, created_courses, errors)

        except Exception as e:
            errors.append(
                {
                    "code": row.get("code"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def get_department(self, department_id):
        """Fetches the department by ID or returns an error."""
        try:
            return Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return {
                "code": None,
                "error": f"Department with ID {department_id} does not exist.",
            }

    def get_session(self, session_id):
        """Fetches the session by ID or returns an error."""
        try:
            return Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return {
                "code": None,
                "error": f"Session with ID {session_id} does not exist.",
            }

    def update_course(self, course, row, department, session, updated_courses, errors):
        """Updates an existing course record."""
        course.name = row["name"]
        course.department = department
        course.session = session
        course.credit_units = row["credit_units"]
        course.description = row["description"]
        course.is_active = row["is_active"]
        course.save()
        updated_courses.append(course.code)

    def create_course(self, row, department, session, created_courses, errors):
        """Creates a new course record."""
        Course.objects.create(
            name=row["name"],
            code=row["code"],
            department=department,
            session=session,
            credit_units=row["credit_units"],
            description=row["description"],
            is_active=row["is_active"],
        )
        created_courses.append(row["code"])
