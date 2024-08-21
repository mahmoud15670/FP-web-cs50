# Generated by Django 4.2.15 on 2024-08-21 17:31

import coursation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursation', '0004_alter_groub_leader_alter_groub_lesson_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lessson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('video', models.FileField(upload_to=coursation.models.lesson_upload_path)),
                ('resource', models.URLField()),
                ('topic', models.TextField()),
            ],
        ),
    ]
