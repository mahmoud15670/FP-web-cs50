# Generated by Django 5.1 on 2024-08-26 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coursation", "0017_lessson_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lessson",
            name="exam",
            field=models.ManyToManyField(null=True, to="coursation.exam"),
        ),
    ]
