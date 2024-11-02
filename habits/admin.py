from django.contrib import admin

from habits.models import Habit, HabitLog

admin.site.register(Habit)
admin.site.register(HabitLog)
