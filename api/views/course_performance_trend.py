from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Course  # Replace with your model for course performance

class CoursePerformanceTrendView(APIView):
    """
    API endpoint to retrieve performance trends for courses.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch or calculate performance trend data
            performance_data = Course.objects.all()

            # Example: Organize data by months or weeks
            trend = []
            labels = []
            for performance in performance_data.order_by('created_at'):  # Replace `timestamp` with your field
                labels.append(performance.created_at.strftime('%B %Y'))  # Example: "December 2024"
                trend.append(performance.id)  # Replace `percentage` with your field

            # Construct the response
            data = {
                "labels": labels,
                "trend": trend
            }
            return Response(data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
