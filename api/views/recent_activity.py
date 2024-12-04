from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now, timedelta
from ..models import ActivityLog

class RecentActivitiesView(APIView):
    """
    API endpoint to retrieve recent activities for the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch activities for the logged-in user
            recent_time_range = now() - timedelta(days=7)  # Last 7 days
            activities = ActivityLog.objects.filter(
                user=request.user,
                timestamp__gte=recent_time_range
            ).order_by('-timestamp')

            # Format the response
            data = [
                {
                    "subject": activity.title,
                    "action": activity.action,
                    "timestamp": activity.timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # Format timestamp
                }
                for activity in activities
            ]

            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
