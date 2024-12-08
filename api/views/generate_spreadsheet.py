from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from ..models import Result

class GenerateSpreadsheetView(APIView):
    """
    Endpoint to generate and download a spreadsheet of result records.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch all results from the database
            results = Result.objects.select_related('student', 'course').all()

            if not results.exists():
                return Response({"error": "No results available to export."}, status=status.HTTP_404_NOT_FOUND)

            # Prepare data for the spreadsheet
            data = [
                {
                    "Student ID": result.student.id,
                    "Student Name": f"{result.student.first_name} {result.student.last_name}",
                    "Course ID": result.course.id,
                    "Course Name": result.course.name,
                    "Score": result.score,
                    "Grade": result.grade,
                    "Uploaded At": result.uploaded_at,
                }
                for result in results
            ]

            # Convert data to a DataFrame
            df = pd.DataFrame(data)

            # Write the DataFrame to an Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Results")

            output.seek(0)

            # Create a response to download the file
            response = HttpResponse(
                output,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=results.xlsx"
            return response

        except Exception as e:
            return Response({"error": f"Error generating spreadsheet: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
