# Generated by Django 5.1 on 2024-08-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "coursation",
            "0007_alter_techer_cv_alter_techer_demo_alter_techer_exams_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="section",
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
                ("name", models.CharField(max_length=20)),
            ],
        ),
    ]
