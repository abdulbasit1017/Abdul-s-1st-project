from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField()
    price = models.IntegerField() 
    description = models.TextField(null=True, blank=True)