from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Habit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    frequency = models.PositiveSmallIntegerField(
        help_text="Enter the number of days between each repetition"
    )
    start_date = models.DateField()
    target = models.PositiveIntegerField(
        null=True, blank=True, help_text="Optional target (e.g., 30 repetitions)"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - Every {self.frequency} days"


class HabitLog(models.Model):
    class HabitStatus(models.TextChoices):
        COMPLETE = "C", "Complete"
        SKIPPED = "S", "Skipped"

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()
    status = models.CharField(
        max_length=1, choices=HabitStatus.choices, default=HabitStatus.COMPLETE
    )

    class Meta:
        unique_together = ("habit", "date")  # Ensures one log per habit per date

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {self.get_status_display()}"
