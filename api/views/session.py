from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q  # For filtering with OR conditions
from ..models import Session
from ..serializers import SessionSerializer

class SessionPagination(PageNumberPagination):
    page_size = 10  # Customize the page size (number of sessions per page)
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional: maximum number of sessions per page

class SessionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Create a new session.
        """
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, session_id=None):
        """
        Retrieve a single session by ID or list all sessions with pagination and search.
        """
        search_term = request.GET.get('search_term', '')  # Get the search query parameter
        
        if session_id:
            try:
                session = Session.objects.get(pk=session_id)
                serializer = SessionSerializer(session)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Session.DoesNotExist:
                return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all sessions with pagination and search
            sessions = Session.objects.all()

            if search_term:
                sessions = sessions.filter(
                    Q(name__icontains=search_term) |  # Search by session name
                    Q(is_active__icontains=search_term)  # Search by session description
                )

            paginator = SessionPagination()
            paginated_sessions = paginator.paginate_queryset(sessions, request)
            serializer = SessionSerializer(paginated_sessions, many=True)
            return paginator.get_paginated_response(serializer.data)

    def put(self, request, session_id=None):
        """
        Update a session by ID.
        """
        try:
            session = Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SessionSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, session_id=None):
        """
        Delete a session by ID.
        """
        try:
            session = Session.objects.get(pk=session_id)
            session.delete()
            return Response({"message": "Session deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
