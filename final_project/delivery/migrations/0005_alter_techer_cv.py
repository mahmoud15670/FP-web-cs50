# Generated by Django 4.2.15 on 2024-08-14 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_alter_techer_cv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techer',
            name='cv',
            field=models.FileField(help_text='please upload a PDF file', upload_to='CV'),
        ),
    ]
