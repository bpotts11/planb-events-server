from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING


class Favorite(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
