from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Student, Course, Result

class DashboardStatsView(APIView):
    """
    API endpoint to retrieve dashboard statistics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            total_students = Student.objects.count()
            total_courses = Course.objects.count()
            results_uploaded = Result.objects.count()

            data = {
                "total_students": total_students,
                "total_courses": total_courses,
                "average_grade": "N/A",
                "results_uploaded": results_uploaded,
            }
            
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

