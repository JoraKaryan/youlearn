from django.db import models
from django.core.validators import RegexValidator
from groups.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='students')
    is_free = models.BooleanField(default=False)
    birthday = models.DateField()
    phone = models.CharField(max_length=15, null=True, default='')
    passport = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
