from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    budget = models.FloatField()
    customer = models.ForeignKey("Category", on_delete=models.CASCADE)
