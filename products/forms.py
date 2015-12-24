from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Seller, Product

class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password',)

class SellerForm(ModelForm):
	class Meta:
		model = Seller
		fields = ('address',)


class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'category', 'price', 'description']




