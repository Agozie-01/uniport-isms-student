from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pandas as pd
from rest_framework.parsers import MultiPartParser
from ..models import Semester  # Only import the Semester model


class UploadSemestersView(APIView):
    """
    Endpoint to upload or update semester records from a spreadsheet.
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

            return self.process_semesters(df)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_file(self, file):
        """Reads the uploaded file and returns a DataFrame or an error response."""
        try:
            df = pd.read_excel(file)
            required_columns = {
                "name", "start_date", "end_date", "description", "is_active"
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

    def process_semesters(self, df):
        """Processes the semester records from the DataFrame."""
        created_semesters = []
        updated_semesters = []
        errors = []

        for _, row in df.iterrows():
            self.process_semester_row(row, created_semesters, updated_semesters, errors)

        return Response(
            {
                "message": "Processing completed.",
                "created_semesters": created_semesters,
                "updated_semesters": updated_semesters,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )

    def process_semester_row(self, row, created_semesters, updated_semesters, errors):
        """Processes a single row of the DataFrame."""
        try:
            existing_semester = Semester.objects.filter(name=row["name"]).first()
            if existing_semester:
                self.update_semester(existing_semester, row, updated_semesters, errors)
            else:
                self.create_semester(row, created_semesters, errors)

        except Exception as e:
            errors.append(
                {
                    "name": row.get("name"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def update_semester(self, semester, row, updated_semesters, errors):
        """Updates an existing semester record."""
        semester.start_date = row["start_date"]
        semester.end_date = row["end_date"]
        semester.description = row["description"]  # Update the description
        semester.is_active = row["is_active"]  # Update the is_active status
        semester.save()
        updated_semesters.append(semester.name)

    def create_semester(self, row, created_semesters, errors):
        """Creates a new semester record."""
        if Semester.objects.filter(name=row["name"]).exists():
            errors.append(
                {
                    "name": row["name"],
                    "error": f"Semester {row['name']} already exists.",
                }
            )
            return

        Semester.objects.create(
            name=row["name"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            description=row["description"],  # Include description when creating
            is_active=row["is_active"],  # Set is_active status
        )
        created_semesters.append(row["name"])
