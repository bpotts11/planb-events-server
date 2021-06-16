from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
