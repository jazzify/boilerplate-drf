# Generated by Django 5.1.5 on 2025-01-27 13:56

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="School",
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
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="SchoolCourse",
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
                ("slug", models.SlugField(max_length=255)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="school_courses",
                        to="school_example.school",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
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
                ("email", models.EmailField(max_length=255)),
                ("identifier", models.UUIDField(default=uuid.uuid4)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="students",
                        to="school_example.school",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Roster",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("active", models.BooleanField(default=True)),
                ("deactivated_at", models.DateField(blank=True, null=True)),
                (
                    "school_course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rosters",
                        to="school_example.schoolcourse",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rosters",
                        to="school_example.student",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="schoolcourse",
            constraint=models.CheckConstraint(
                condition=models.Q(("start_date__lt", models.F("end_date"))),
                name="school_course_start_before_end",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="schoolcourse",
            unique_together={("name", "slug", "start_date", "end_date")},
        ),
        migrations.AlterUniqueTogether(
            name="student",
            unique_together={("email", "school"), ("identifier", "school")},
        ),
        migrations.AddConstraint(
            model_name="roster",
            constraint=models.CheckConstraint(
                condition=models.Q(("start_date__lt", models.F("end_date"))),
                name="roster_start_before_end",
            ),
        ),
    ]
