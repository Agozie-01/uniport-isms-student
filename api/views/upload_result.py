from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pandas as pd
from rest_framework.parsers import MultiPartParser
from ..models import Result, Student, Course


class UploadResultsView(APIView):
    """
    Endpoint to upload or update result records from a spreadsheet.
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

            return self.process_results(df)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_file(self, file):
        """Reads the uploaded file and returns a DataFrame or an error response."""
        try:
            df = pd.read_excel(file)
            required_columns = {
                "student_id", "course_id", "score", "grade"
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

    def process_results(self, df):
        """Processes the result records from the DataFrame."""
        created_results = []
        updated_results = []
        errors = []

        for _, row in df.iterrows():
            self.process_result_row(row, created_results, updated_results, errors)

        return Response(
            {
                "message": "Processing completed.",
                "created_results": created_results,
                "updated_results": updated_results,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )

    def process_result_row(self, row, created_results, updated_results, errors):
        """Processes a single row of the DataFrame."""
        try:
            student = Student.objects.filter(id=row["student_id"]).first()
            course = Course.objects.filter(id=row["course_id"]).first()

            if not student:
                errors.append(
                    {
                        "student_id": row["student_id"],
                        "error": "Student not found.",
                    }
                )
                return

            if not course:
                errors.append(
                    {
                        "course_id": row["course_id"],
                        "error": "Course not found.",
                    }
                )
                return

            existing_result = Result.objects.filter(student=student, course=course).first()
            if existing_result:
                self.update_result(existing_result, row, updated_results)
            else:
                self.create_result(student, course, row, created_results)

        except Exception as e:
            errors.append(
                {
                    "student_id": row.get("student_id"),
                    "course_id": row.get("course_id"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def update_result(self, result, row, updated_results):
        """Updates an existing result record."""
        result.score = row["score"]
        result.grade = row["grade"]
        result.save()
        updated_results.append({"student": result.student.id, "course": result.course.id})

    def create_result(self, student, course, row, created_results):
        """Creates a new result record."""
        Result.objects.create(
            student=student,
            course=course,
            score=row["score"],
            grade=row["grade"],
        )
        created_results.append({"student": student.id, "course": course.id})
