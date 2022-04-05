from statistics import mode
from tkinter import CASCADE
from django.db import models
from authentication.models import User
# Create your models here.


class url(models.Model):
    uuid = models.CharField(max_length=10)
    long_url = models.CharField(max_length=200)
    impressions = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.long_url
