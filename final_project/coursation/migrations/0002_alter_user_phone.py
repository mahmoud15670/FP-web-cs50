# Generated by Django 4.2.15 on 2024-08-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='phone'),
        ),
    ]
