from django.db import models


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    duration = models.CharField(max_length=50, default='3 months')
    price = models.IntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name