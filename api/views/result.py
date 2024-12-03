from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from ..serializers import AdminSerializer

class AdminView(APIView):
    permission_classes = [IsAuthenticated]  # Default for the whole view

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]  # Allow all users for POST
        return [IsAuthenticated()]  # Require authentication for other methods

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
