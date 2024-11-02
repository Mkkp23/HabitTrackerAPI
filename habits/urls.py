from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from habits.views import (
    HabitListCreateAPIView,
    HabitRetrieveUpdateDestroyAPIView,
    HabitLogCreateListAPIView,
    HabitlogRetrieveDestroyAPIView,
    HabitStatisticsView,
)

urlpatterns = [
    path("token/get/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("habits/", HabitListCreateAPIView.as_view(), name="habit_list_create"),
    path(
        "habits/<int:pk>/",
        HabitRetrieveUpdateDestroyAPIView.as_view(),
        name="habit_detail",
    ),
    path("habits/<int:pk>/log/", HabitLogCreateListAPIView.as_view(), name="habit_log"),
    path("habits/stats/", HabitStatisticsView.as_view(), name="habit_stats"),
    path(
        "habitlog/<int:pk>/",
        HabitlogRetrieveDestroyAPIView.as_view(),
        name="habitlog_detail",
    ),
]
