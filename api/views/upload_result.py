from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser
import pandas as pd
from ..models import Result, Student, Course, Session

# Define the column mapping
COLUMN_MAP = {
    "s/no": "s_no",
    "mat no": "matric_number",
    "name": "name",
    "course code": "course_code",
    "total score": "score",
}

# Required columns after mapping
REQUIRED_COLUMNS = {"matric_number", "score"}

class UploadResultsView(APIView):
    """
    Endpoint to upload or update result records from a spreadsheet.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        course_code = request.data.get("course")  # Capture course from request
        session_name = request.data.get("session")  # Capture session from request

        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not course_code:
            return Response({"error": "Course is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not session_name:
            return Response({"error": "Session is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate course exists
        course = Course.objects.filter(code=course_code).first()
        if not course:
            return Response({"error": "Invalid course selected"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate session exists
        session = Session.objects.filter(name=session_name).first()
        if not session:
            return Response({"error": "Invalid session selected"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = self.read_file(file)
            if isinstance(df, Response):
                return df  # If read_file returns an error response, return it

            return self.process_results(df, course, session)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_file(self, file):
        """Reads the uploaded file and returns a DataFrame or an error response."""
        try:
            df = pd.read_excel(file, header=None)  # Read without assuming headers
            
            # Identify the row containing 'mat no' or its variations
            matric_variants = {"matric_no", "matric no", "matric_number", "mat no"}
            header_row_index = None

            for i, row in df.iterrows():
                row_values = [str(val).strip().lower() for val in row.fillna("")]
                if any(col in row_values for col in matric_variants):
                    header_row_index = i
                    break

            if header_row_index is None:
                return Response(
                    {"error": "Could not detect header row with 'matric number' column."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set the detected row as the header
            df.columns = df.iloc[header_row_index]
            df = df[header_row_index + 1:].reset_index(drop=True)

            # Normalize column names
            df.columns = [col.strip().lower() for col in df.columns]

            # Rename variations of 'matric_number' to a standard format
            for col in df.columns:
                if col in matric_variants:
                    df.rename(columns={col: "matric_number"}, inplace=True)
                    break  # Stop once a match is found

            # Rename columns using predefined mapping
            df.rename(columns=COLUMN_MAP, inplace=True)

            # Validate required columns
            missing_required = REQUIRED_COLUMNS - set(df.columns)
            if missing_required:
                return Response(
                    {"error": f"Missing required columns: {missing_required}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if "status" not in df.columns:
                df["status"] = "pending"  # Default status if missing

            return df
        except Exception as e:
            return Response({"error": f"Error reading file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def process_results(self, df, course, session):
        """Processes the result records from the DataFrame."""
        created_results = []
        updated_results = []
        errors = []

        for _, row in df.iterrows():
            self.process_result_row(row, course, session, created_results, updated_results, errors)

        return Response(
            {
                "message": "Processing completed.",
                "created_results": created_results,
                "updated_results": updated_results,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )

    def process_result_row(self, row, course, session, created_results, updated_results, errors):
        """Processes a single row of the DataFrame."""
        try:
            student = Student.objects.filter(matric_number=row["matric_number"]).first() or \
                     Student.objects.filter(email=row["matric_number"]).first()

            if not student:
                errors.append({"matric_number": row["matric_number"], "error": "Student not found."})
                return

            existing_result = Result.objects.filter(student=student, course=course, session=session).first()
            if existing_result:
                self.update_result(existing_result, row, updated_results)
            else:
                self.create_result(student, course, session, row, created_results)

        except Exception as e:
            errors.append(
                {
                    "matric_number": row.get("matric_number"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def update_result(self, result, row, updated_results):
        """Updates an existing result record."""
        result.score = row["score"]
        result.status = row["status"]
        result.save()
        updated_results.append({"student": result.student.id, "course": result.course.id, "session": result.session.id})

    def create_result(self, student, course, session, row, created_results):
        """Creates a new result record."""
        Result.objects.create(
            student=student,
            course=course,
            session=session,
            score=row["score"],
            status=row["status"],
        )
        created_results.append({"student": student.id, "course": course.id, "session": session.id})
