from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..models import Semester
from ..serializers import SemesterSerializer

class SemesterView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Create a new semester.
        """
        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, semester_id=None):
        """
        Retrieve a single semester by ID or list all semesters.
        """
        if semester_id:
            try:
                semester = Semester.objects.get(pk=semester_id)
                serializer = SemesterSerializer(semester)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Semester.DoesNotExist:
                return Response({"error": "Semester not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # List all semesters
            semesters = Semester.objects.all()
            serializer = SemesterSerializer(semesters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, semester_id=None):
        """
        Update a semester by ID.
        """
        try:
            semester = Semester.objects.get(pk=semester_id)
        except Semester.DoesNotExist:
            return Response({"error": "Semester not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SemesterSerializer(semester, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, semester_id=None):
        """
        Delete a semester by ID.
        """
        try:
            semester = Semester.objects.get(pk=semester_id)
            semester.delete()
            return Response({"message": "Semester deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Semester.DoesNotExist:
            return Response({"error": "Semester not found"}, status=status.HTTP_404_NOT_FOUND)
