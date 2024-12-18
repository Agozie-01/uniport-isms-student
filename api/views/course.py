from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q  # For filtering with OR conditions
from ..models import Course
from ..serializers import CourseSerializer

class CoursePagination(PageNumberPagination):
    page_size = 10  # Customize the page size (number of courses per page)
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional: maximum number of courses per page

class CourseView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Create a new course.
        """
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, course_id=None):
        """
        Retrieve a single course by ID or list all courses with pagination and search.
        """
        search_term = request.GET.get('search_term', '')  # Get the search query parameter
        
        if course_id:
            try:
                course = Course.objects.get(pk=course_id)
                serializer = CourseSerializer(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Course.DoesNotExist:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all courses with pagination and search
            courses = Course.objects.all()

            if search_term:
                courses = courses.filter(
                    Q(code__icontains=search_term) |  # Search by course code
                    Q(name__icontains=search_term) | # Search by course title
                    Q(description__icontains=search_term) # Search by description
                )

            paginator = CoursePagination()
            paginated_courses = paginator.paginate_queryset(courses, request)
            serializer = CourseSerializer(paginated_courses, many=True)
            return paginator.get_paginated_response(serializer.data)

    def put(self, request, course_id=None):
        """
        Update a course by ID.
        """
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id=None):
        """
        Delete a course by ID.
        """
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
