from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


from habits.models import Habit, HabitLog
from habits.serializers import HabitSerializer, HabitLogSerializer


# Class for modifying pagination
class CustomPagination(PageNumberPagination):
    page_size = 5


class HabitListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ["frequency", "start_date"]
    search_fields = ["name", "description"]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitLogCreateListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        # Fetch the habit instance and ensure it belongs to the authenticated user
        habit = get_object_or_404(Habit, pk=pk, user=request.user)
        habit_logs = HabitLog.objects.filter(habit=habit)
        serializer = HabitLogSerializer(habit_logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        # Fetch the habit instance and ensure it belongs to the authenticated user
        habit = get_object_or_404(Habit, pk=pk, user=request.user)

        # Initialize the serializer
        serializer = HabitLogSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Save the habit log, passing the habit instance
                serializer.save(habit=habit)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {
                        "error": "A log entry for this habit on this date already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HabitlogRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = HabitLog.objects.all()
    serializer_class = HabitLogSerializer

    def get_queryset(self):
        return HabitLog.objects.filter(habit__user=self.request.user)


class HabitStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Total number of habits
        total_habits = Habit.objects.filter(user=user).count()

        # Total number of habit logs
        total_logs = HabitLog.objects.filter(habit__user=user).count()

        # Completed habits: count unique habits that have been logged as complete
        completed_habits = (
            HabitLog.objects.filter(
                habit__user=user, status=HabitLog.HabitStatus.COMPLETE
            )
            .values("habit")
            .distinct()
            .count()
        )

        # Completion rate
        completion_rate = (completed_habits / total_logs) * 100 if total_logs > 0 else 0

        # Constructing the response data
        stats = {
            "total_habits": total_habits,
            "completed_habits": completed_habits,
            "total_logs": total_logs,
            "completion_rate": completion_rate,
        }

        return Response(stats, status=status.HTTP_200_OK)
