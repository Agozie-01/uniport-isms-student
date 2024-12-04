from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import AdminSerializer

class CurrentUserView(APIView):
    """
    API endpoint to retrieve the currently logged-in admin's details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        admin = request.user  # Retrieve the currently logged-in user
        serializer = AdminSerializer(admin)
        return Response(serializer.data)
