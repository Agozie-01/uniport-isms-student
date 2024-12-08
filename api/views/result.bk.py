from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse
from io import BytesIO
import pandas as pd

from ..models import Result, Student, Course
from ..serializers import ResultSerializer


class FetchResultsView(APIView):
    """
    Endpoint to fetch all results.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateSpreadsheetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            # Fetch all results for the given student
            student = Student.objects.get(id=student_id)
            results = Result.objects.filter(student=student)
            
            # Validate that results exist
            if not results.exists():
                return Response({"message": "No results found for this student"}, status=status.HTTP_404_NOT_FOUND)
            
            # Generate spreadsheet logic here
            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = f"attachment; filename={student_id}_results.xlsx"
            
            # Example: Generate a basic spreadsheet using openpyxl or similar library
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = f"{student.name}'s Results"

            # Add headers
            ws.append(["Course", "Score", "Grade", "Uploaded At"])
            
            # Add data rows
            for result in results:
                ws.append([result.course.name, result.score, result.grade, result.uploaded_at])
            
            # Save the spreadsheet to the response
            wb.save(response)
            return response
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


class UploadResultsView(APIView):
    """
    Endpoint to upload results from a spreadsheet.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the spreadsheet using pandas
            df = pd.read_excel(file)

            # Process each row in the DataFrame
            for _, row in df.iterrows():
                student = Student.objects.get(id=row["student_id"])  # Assuming the column is 'student_id'
                course = Course.objects.get(id=row["course_id"])  # Assuming the column is 'course_id'

                result_data = {
                    "student": student,
                    "course": course,
                    "score": row["score"],
                    "grade": row["grade"],
                }

                # Save the result to the database
                Result.objects.create(**result_data)

            return Response({"message": "Results uploaded successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
