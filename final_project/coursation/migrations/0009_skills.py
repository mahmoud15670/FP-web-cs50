# Generated by Django 4.2.15 on 2024-08-25 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursation', '0008_alter_user_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
    ]
