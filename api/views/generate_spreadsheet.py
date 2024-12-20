from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from ..models import Result

class GenerateSpreadsheetView(APIView):
    """
    Endpoint to generate and download a spreadsheet of result records.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, student_id=None):
        try:
            # Filter results by student_id from the URL
            results = Result.objects.select_related('student', 'course')
            if student_id:
                results = results.filter(student_id=student_id)

            if not results.exists():
                return HttpResponse(
                    "No results available to export.",
                    content_type="text/plain",
                    status=404
                )

            # Prepare data for the spreadsheet
            data = [
                {
                    "Student ID": result.student.id,
                    "Student Name": f"{result.student.first_name} {result.student.last_name}",
                    "Course ID": result.course.id,
                    "Course Name": result.course.name,
                    "Score": result.score,
                    "Grade": result.grade,
                    "Uploaded At": result.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                for result in results
            ]

            # Convert data to DataFrame and generate the response
            df = pd.DataFrame(data)

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Results")

            output.seek(0)

            # Create a response to download the file
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=results.xlsx"
            return response

        except Exception as e:
            return HttpResponse(
                f"Error generating spreadsheet: {str(e)}",
                content_type="text/plain",
                status=500
            )
