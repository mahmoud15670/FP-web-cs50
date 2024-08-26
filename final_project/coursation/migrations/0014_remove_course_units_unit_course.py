# Generated by Django 4.2.15 on 2024-08-26 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursation', '0013_alter_course_cirtification_alter_course_review_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='units',
        ),
        migrations.AddField(
            model_name='unit',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='coursation.course'),
            preserve_default=False,
        ),
    ]
