from django.db import models

class Seller(models.Model):
	name = models.CharField(max_length=500)
	address = models.CharField(max_length=200)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)

class Product(models.Model):
	seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
	category = models.CharField(max_length=500)
	geolocation = Seller(pk=seller).address
	price = models.IntegerField(default=0)
	sold = models.BooleanField(default=True)
	description = models.TextField(max_length=1000)

