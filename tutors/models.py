from django.db import models


class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    experience = models.IntegerField(default=0)
    information = models.CharField(max_length=50, default='')

    def __str__(self):
        return f"{self.name} {self.surname}"