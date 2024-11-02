from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from habits.models import Habit, HabitLog
from habits.serializers import HabitSerializer, HabitLogSerializer


class HabitListCreateAPIView(ListCreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
