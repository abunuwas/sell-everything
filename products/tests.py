from django.test import TestCase
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse

from .models import Seller, User, Product


class CreateSellerTest(TestCase):
	def setUp(self):
		jesus = User(first_name='Jesus', 
					 last_name='Christ', 
					 username='jesus',
					 email='jesus@jesus.com',
					 password='asdf1234')
		jesus.set_password(jesus.password)
		jesus.save()
		jesusSeller = Seller(user=jesus, address='Bethlem')

		richie = User(first_name='Riche', 
					 last_name='Ober', 
					 username='richie',
					 email='richie@richie.com',
					 password='asdf1234')
		jesus.set_password(jesus.password)
		jesus.save()
		jesusSeller = Seller(user=jesus, address='Frankfurt an der Oder')


class registerUser(TestCase):
	pass

