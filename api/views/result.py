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
    """
    Endpoint to generate and download a spreadsheet of results.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = Result.objects.all()
        data = ResultSerializer(results, many=True).data

        # Convert data to a DataFrame
        df = pd.DataFrame(data)

        # Convert DataFrame to Excel format in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')

        # Prepare the response to download the file
        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=student_results.xlsx'
        return response


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
