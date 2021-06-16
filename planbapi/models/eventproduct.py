from django.db import models


class EventProduct(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
