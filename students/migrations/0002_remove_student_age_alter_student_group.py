# Generated by Django 5.1.3 on 2024-11-30 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='age',
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.IntegerField(),
        ),
    ]
