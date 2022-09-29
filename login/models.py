from django.db import models


# Create your models here.
class Sistema(models.Model):
    primerInicio = models.BooleanField(default=True)