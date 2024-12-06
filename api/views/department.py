from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q  # For filtering with OR conditions
from ..models import Department
from ..serializers import DepartmentSerializer

class DepartmentPagination(PageNumberPagination):
    page_size = 10  # Customize the page size (number of departments per page)
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional: maximum number of departments per page

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
        Retrieve a single department by ID or list all departments with pagination and search.
        """
        search_term = request.GET.get('search_term', '')  # Get the search query parameter
        
        if department_id:
            try:
                department = Department.objects.get(pk=department_id)
                serializer = DepartmentSerializer(department)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Department.DoesNotExist:
                return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all departments with pagination and search
            departments = Department.objects.all()

            if search_term:
                departments = departments.filter(
                    Q(name__icontains=search_term) |  # Search by department name
                    Q(code__icontains=search_term)  # Search by description
                )

            paginator = DepartmentPagination()
            paginated_departments = paginator.paginate_queryset(departments, request)
            serializer = DepartmentSerializer(paginated_departments, many=True)
            return paginator.get_paginated_response(serializer.data)

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
