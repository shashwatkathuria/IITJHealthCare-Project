from django.db import models

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length = 150)
    company = models.CharField(max_length = 150)
    expiryDate = models.DateField()
    manufacturedDate = models.DateField()
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return "Name : " + str(self.name) + " Company : " + str(self.company) + " Manufactured Date : " + str(self.manufacturedDate) + " Expiry Date : " + str(self.expiryDate) + " Quantity : " + str(self.quantity)
