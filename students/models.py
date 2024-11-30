from django.db import models

from django.db import models
from django.core.validators import RegexValidator

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    group = models.IntegerField()
    is_free = models.BooleanField(default=False)
    birthday = models.DateField()
    phone = models.CharField(max_length=15, null=True)
    passport = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
