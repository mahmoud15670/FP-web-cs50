# Generated by Django 4.2.15 on 2024-08-28 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coursation', '0020_alter_lessson_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessson',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coursation.unit'),
        ),
    ]
