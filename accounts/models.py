from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superuser', 'Superuser'),
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    # Related names to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Specify a unique related_name
        blank=True,
        # help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Specify a unique related_name
        blank=True,
        # help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def is_tutor(self):
        return self.role == 'tutor'

    def is_student(self):
        return self.role == 'student'
