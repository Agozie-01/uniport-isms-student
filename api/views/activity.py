from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ActivityView(APIView):
    """
    API endpoint to retrieve user activities
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
       pass
