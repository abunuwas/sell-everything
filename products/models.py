from django.db import models

class Seller(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	email = models.EmailField(max_length=50)
	password = models.CharField(max_length=10)

	def __str__(self):
		return self.email

class Product(models.Model):
	seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	category = models.CharField(max_length=100)
	geolocation = Seller(pk=seller).address
	price = models.IntegerField(default=0)
	sold = models.BooleanField(default=False)
	description = models.TextField(max_length=1000)
	created = models.DateTimeField('date created')

	def __str__(self):
		return self.title

