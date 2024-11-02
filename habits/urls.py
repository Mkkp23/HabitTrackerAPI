from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from habits.views import HabitListCreateAPIView

urlpatterns = [
    path("token/get/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("habits/", HabitListCreateAPIView.as_view(), name="habit_list_create"),
]
