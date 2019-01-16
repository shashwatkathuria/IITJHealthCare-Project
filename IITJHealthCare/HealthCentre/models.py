from django.db import models

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(max_length = 10)
    email = models.CharField(max_length = 30)

class Patient(models.Model):
    name = models.CharField(max_length = 30)
    address = models.CharField(max_length = 100)
    contactNumber = models.CharField(max_length = 10)
    email = models.CharField(max_length = 30)
