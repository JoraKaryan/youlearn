# Generated by Django 4.2.16 on 2024-12-06 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_delete_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.CharField(default='3 months', max_length=50),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
