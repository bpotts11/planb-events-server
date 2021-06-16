from django.db import models
from django.contrib.auth.models import User


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    business_name = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=55)
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=2)
