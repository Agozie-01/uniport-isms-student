from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from ..models import Result
from ..serializers import ResultSerializer


class ResultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ResultView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Create a new result.
        """
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, result_id=None):
        """
        Retrieve a single result by ID or list all results with pagination and search.
        """
        search_term = request.GET.get('search_term', '')

        if result_id:
            try:
                result = Result.objects.get(pk=result_id)
                serializer = ResultSerializer(result)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Result.DoesNotExist:
                return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            results = Result.objects.all()

            if search_term:
                results = results.filter(
                    Q(student__first_name__icontains=search_term) |
                    Q(course__name__icontains=search_term)
                )

            paginator = ResultPagination()
            paginated_results = paginator.paginate_queryset(results, request)
            serializer = ResultSerializer(paginated_results, many=True)
            return paginator.get_paginated_response(serializer.data)

    def put(self, request, result_id=None):
        """
        Update a result by ID.
        """
        try:
            result = Result.objects.get(pk=result_id)
        except Result.DoesNotExist:
            return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResultSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, result_id=None):
        """
        Delete a result by ID.
        """
        try:
            result = Result.objects.get(pk=result_id)
            result.delete()
            return Response({"message": "Result deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Result.DoesNotExist:
            return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)
