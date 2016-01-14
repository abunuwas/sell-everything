from django.test import TestCase
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest

from .views import IndexView, register, Login, logout_view, LoggedIn, removeProduct, AddProduct, EditProduct
from .models import Seller, User, Product

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = IndexView()
		
#		richie = User(first_name='Riche', 
#					 last_name='Ober', 
#					 username='richie',
#					 email='richie@richie.com',
#					 password='asdf1234')
#		jesus.set_password(jesus.password)
#		jesus.save()
#		jesusSeller = Seller(user=jesus, address='Frankfurt an der Oder')


#class registerUser(TestCase):
#	pass


#class CreateSellerTest(TestCase):
#	def setUp(self):
#		jesus = User(first_name='Jesus', 
#					 last_name='Christ', 
#					 username='jesus',
#					 email='jesus@jesus.com',
#					 password='asdf1234')
#		jesus.set_password(jesus.password)
#		jesus.save()
#		jesusSeller = Seller(user=jesus, address='Bethlem')
#