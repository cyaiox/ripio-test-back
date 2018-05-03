from django.db import models


# Create your models here.
class Coin(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    symbol = models.CharField(max_length=5)

    def __str__(self):
        return self.name
