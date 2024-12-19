from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    experience = models.IntegerField(default=0)
    information = models.CharField(max_length=50, default='')

    def __str__(self):
        return f"{self.name} {self.surname}"