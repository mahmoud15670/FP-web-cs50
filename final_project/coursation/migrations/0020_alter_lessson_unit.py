# Generated by Django 4.2.15 on 2024-08-28 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursation', '0019_course_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessson',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='coursation.unit'),
        ),
    ]
