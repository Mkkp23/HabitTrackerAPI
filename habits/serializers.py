from rest_framework import serializers
from habits.models import Habit, HabitLog

class HabitSerializer(serializers.ModelSerializer):
    # Display the username for the user field as read-only
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Habit
        fields = ("id", "name", "description", "frequency", "start_date", "target", "user")

    def validate_frequency(self, value):
        if value > 20:
            raise serializers.ValidationError(
                "Habits that take more than 20 days to repeat are lame :)"
            )
        return value


class HabitLogSerializer(serializers.ModelSerializer):
    # Nested representation for the habit foreign key
    habit = serializers.StringRelatedField()

    class Meta:
        model = HabitLog
        fields = ("id", "habit", "date", "status")
