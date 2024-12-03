from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..models import Department
from ..serializers import DepartmentSerializer

class DepartmentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Create a new department.
        """
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, department_id=None):
        """
        Retrieve a single department by ID or list all departments.
        """
        if department_id:
            try:
                department = Department.objects.get(pk=department_id)
                serializer = DepartmentSerializer(department)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Department.DoesNotExist:
                return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all departments
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, department_id=None):
        """
        Update a department by ID.
        """
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, department_id=None):
        """
        Delete a department by ID.
        """
        try:
            department = Department.objects.get(pk=department_id)
            department.delete()
            return Response({"message": "Department deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
