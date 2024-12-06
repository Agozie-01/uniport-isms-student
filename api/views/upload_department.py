from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pandas as pd
from rest_framework.parsers import MultiPartParser
from ..models import Department  # Import the Department model

class UploadDepartmentsView(APIView):
    """
    Endpoint to upload or update department records from a spreadsheet.
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

            return self.process_departments(df)

        except Exception as e:
            return Response({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def read_file(self, file):
        """Reads the uploaded file and returns a DataFrame or an error response."""
        try:
            df = pd.read_excel(file)  # Assuming Excel is used for consistency
            required_columns = {"name", "code"}  # Required columns
            if not required_columns.issubset(df.columns):
                missing_columns = required_columns - set(df.columns)
                return Response(
                    {"error": f"Missing required columns: {missing_columns}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return df
        except Exception as e:
            return Response({"error": f"Error reading file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def process_departments(self, df):
        """Processes the department records from the DataFrame."""
        created_departments = []
        updated_departments = []
        errors = []

        for _, row in df.iterrows():
            self.process_department_row(row, created_departments, updated_departments, errors)

        return Response(
            {
                "message": "Processing completed.",
                "created_departments": created_departments,
                "updated_departments": updated_departments,
                "errors": errors,
            },
            status=status.HTTP_200_OK,
        )

    def process_department_row(self, row, created_departments, updated_departments, errors):
        """Processes a single row of the DataFrame."""
        try:
            existing_department = Department.objects.filter(code=row["code"]).first()
            if existing_department:
                self.update_department(existing_department, row, updated_departments, errors)
            else:
                self.create_department(row, created_departments, errors)

        except Exception as e:
            errors.append(
                {
                    "name": row.get("name"),
                    "error": f"Error processing record: {str(e)}",
                }
            )

    def update_department(self, department, row, updated_departments, errors):
        """Updates an existing department record."""
        department.name = row["name"]
        department.save()
        updated_departments.append(department.name)

    def create_department(self, row, created_departments, errors):
        """Creates a new department record."""
        if Department.objects.filter(code=row["code"]).exists():
            errors.append(
                {
                    "name": row["name"],
                    "error": f"Department with code {row['code']} already exists.",
                }
            )
            return

        Department.objects.create(
            name=row["name"],
            code=row["code"],
        )
        created_departments.append(row["name"])
