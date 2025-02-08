# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_admin(self):
        return self.role == 'admin'

    def is_tutor(self):
        return self.role == 'tutor'

    def is_student(self):
        return self.role == 'student'

    def save(self, *args, **kwargs):
        # Automatically set role to 'admin' for superusers
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)