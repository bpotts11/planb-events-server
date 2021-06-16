from django.db import models


class ProductTag(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
