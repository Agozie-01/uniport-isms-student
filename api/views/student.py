from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q  # Add this import
from ..models import Student
from ..serializers import StudentSerializer
from ..utils import log_activity

class StudentView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        """
        Create a new student.
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, student_id=None):
        """
        Retrieve a single student by ID or list all students with pagination and search.
        """
        log_activity(request.user, "Get User", "List Single User")

        if student_id:
            try:
                student = Student.objects.get(pk=student_id)
                serializer = StudentSerializer(student)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Student.DoesNotExist:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Search term
            search_term = request.query_params.get('search_term', '').strip()

            # Queryset
            students = Student.objects.all()
            if search_term:
                students = students.filter(
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term) |
                    Q(matric_number__icontains=search_term) |
                    Q(email__icontains=search_term)
                )

            # Paginate the list of students
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Number of students per page (adjust as needed)
            result_page = paginator.paginate_queryset(students, request)
            serializer = StudentSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def put(self, request, student_id=None):
        """
        Update a student by ID.
        """
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, student_id=None):
        """
        Delete a student by ID.
        """
        try:
            student = Student.objects.get(pk=student_id)
            student.delete()
            return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
