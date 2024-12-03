from django.db import models
from tutors.models import Tutor
from courses.models import Course


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    duration = models.CharField(max_length=50, default='3 months')
    price = models.IntegerField(default=0)  # Default price to 0
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, related_name='groups')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.name