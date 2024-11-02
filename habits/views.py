from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

from habits.models import Habit, HabitLog
from habits.serializers import HabitSerializer, HabitLogSerializer


class HabitListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitLogCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

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
