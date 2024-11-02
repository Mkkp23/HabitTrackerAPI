# Generated by Django 5.1.2 on 2024-11-02 07:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "frequency",
                    models.PositiveSmallIntegerField(
                        help_text="Enter the number of days between each repetition"
                    ),
                ),
                ("start_date", models.DateField()),
                (
                    "target",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Optional target (e.g., 30 repetitions)",
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HabitLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[("C", "Complete"), ("S", "Skipped")],
                        default="S",
                        max_length=1,
                    ),
                ),
                (
                    "habit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logs",
                        to="habits.habit",
                    ),
                ),
            ],
            options={
                "unique_together": {("habit", "date")},
            },
        ),
    ]
