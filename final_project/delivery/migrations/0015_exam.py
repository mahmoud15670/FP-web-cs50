# Generated by Django 5.1 on 2024-08-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0014_remove_stage_student_remove_stage_techer_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exam",
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
                ("date", models.DateTimeField()),
                ("total", models.SmallIntegerField()),
                ("degree", models.SmallIntegerField()),
                ("duration", models.CharField(max_length=12)),
                ("question", models.TextField()),
                ("answer", models.TextField()),
            ],
        ),
    ]
