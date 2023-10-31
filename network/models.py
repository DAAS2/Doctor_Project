from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Doctor(models.Model):
    name = models.TextField()
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.TextField()
    working_status = models.TextField()
    profession = models.TextField()
    country = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


