from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pandas as pd
from rest_framework.parsers import MultiPartParser
from ..models import Session, Semester  # Import Session and Semester models


class UploadSessionsView(APIView):
    """
    Endpoint to upload or update session records from a spreadsheet.
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

            return self.process_sessions(df)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_file(self, file):
        """Reads the uploaded file and returns a DataFrame or an error response."""
        try:
            df = pd.read_excel(file)
            required_columns = {
                "name", "semester", "start_date", "end_date", "is_active"
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

    def process_sessions(self, df):
        """Processes the session records from the DataFrame."""
        created_sessions = []
        updated_sessions = []
        errors = []

        for _, row in df.iterrows():
            self.process_session_row(row, created_sessions, updated_sessions, errors)

        return Response(
            {
                "message": "Processing completed.",
                "created_sessions": created_sessions,
                "updated_sessions": updated_sessions,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )

    def process_session_row(self, row, created_sessions, updated_sessions, errors):
        """Processes a single row of the DataFrame."""
        try:
            # Find the semester related to this session by its name
            semester = Semester.objects.filter(name=row["semester"]).first()
            if not semester:
                errors.append(
                    {
                        "name": row.get("name"),
                        "error": f"Semester {row['semester']} does not exist.",
                    }
                )
                return

            existing_session = Session.objects.filter(name=row["name"], semester=semester).first()
            if existing_session:
                self.update_session(existing_session, row, updated_sessions, errors)
            else:
                self.create_session(row, semester, created_sessions, errors)

        except Exception as e:
            errors.append(
                {
                    "name": row.get("name"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def update_session(self, session, row, updated_sessions, errors):
        """Updates an existing session record."""
        session.start_date = row["start_date"]
        session.end_date = row["end_date"]
        session.is_active = row["is_active"]
        session.save()
        updated_sessions.append(session.name)

    def create_session(self, row, semester, created_sessions, errors):
        """Creates a new session record."""
        if Session.objects.filter(name=row["name"], semester=semester).exists():
            errors.append(
                {
                    "name": row["name"],
                    "error": f"Session {row['name']} for semester {semester.name} already exists.",
                }
            )
            return

        Session.objects.create(
            name=row["name"],
            semester=semester,
            start_date=row["start_date"],
            end_date=row["end_date"],
            is_active=row["is_active"],
        )
        created_sessions.append(row["name"])
