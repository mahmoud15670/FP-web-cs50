# Generated by Django 4.2.15 on 2024-08-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='techer',
            name='phone',
            field=models.CharField(default='010', max_length=11),
            preserve_default=False,
        ),
    ]
