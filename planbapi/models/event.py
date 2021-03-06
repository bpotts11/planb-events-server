from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    budget = models.FloatField()
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    products = models.ManyToManyField(
        "Product", through="EventProduct", related_name="products")
