from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..models import Admin
from ..serializers import AdminSerializer

class AdminView(APIView):
    permission_classes = [IsAdminUser]  # Restrict access to admin users only

    def post(self, request):
        """
        Create a new admin.
        """
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, admin_id=None):
        """
        Retrieve a single admin by ID or list all admins.
        """
        if admin_id:
            try:
                admin = Admin.objects.get(pk=admin_id)
                serializer = AdminSerializer(admin)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Admin.DoesNotExist:
                return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all admins
            admins = Admin.objects.all()
            serializer = AdminSerializer(admins, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, admin_id=None):
        """
        Update an admin by ID.
        """
        try:
            admin = Admin.objects.get(pk=admin_id)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, admin_id=None):
        """
        Delete an admin by ID.
        """
        try:
            admin = Admin.objects.get(pk=admin_id)
            admin.delete()
            return Response({"message": "Admin deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
