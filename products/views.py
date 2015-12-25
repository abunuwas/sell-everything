from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import generic
#from django.template import RequestContext

from .models import Seller, Product
from .forms import UserForm, SellerForm, LoginForm

class IndexView(generic.ListView):
	template_name = 'products/index.html'
	context_object_name = 'products_list'

	def get_queryset(self):
		return Product.objects.order_by('-created')[:5]

def filterProducts(request, productFilter):
	response = "You're at products which belong to the %s category."
	return HttpResponse(response % productFilter)

def detailProduct(request, product_id):
	return HttpResponse("You've viewing the details of product %s" % product_id)

def buyProduct(request, product_id):
	return HttpResponse("You've purchased product %s" % product_id)

def register(request):
	#context = RequestContext(request)
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		seller_form = SellerForm(data=request.POST)
		if user_form.is_valid() and seller_form.is_valid():
			user = user_form.save()
			user.set_password(user.password) #hashes the password with the set_password method
			user.save()
			seller = seller_form.save()
			seller.user = user
			registered = True
			#seller = authenticate(username=user.username, password=user.password)
			#print(seller, ' for %s and %s' % (user.username, user.password))
			#login(request, seller)
			if user.first_name:
				firstName = user.first_name
			else:
				firstName = user.username
			return render(request, 'products/loggedin.html', {'first_name': firstName})
	else:
		user_form = UserForm()
		seller_form = SellerForm()
	return render(request, 'products/registration.html', 
		           {'user_form': user_form, 'seller_form': seller_form, 'registered': registered}
		           )

def logIn(request):
	#context = RequestContext(request)
	if request.method == 'POST':
		seller_form = LoginForm(data=request.POST)
		if seller_form.is_valid():
			cd = seller_form.cleaned_data
			username = cd['username']
			pwd = cd['password']
			seller = authenticate(username=username, password=pwd)
			print('seller is ', seller)
			if seller is not None:
				print('We have seller')
				if seller.is_active:
					print('Account is active')
					login(request, seller)
					if seller.first_name:
						firstName = seller.first_name
					else:
						firstName = seller.username
					return render(request, 'products/loggedin.html', {'first_name': firstName})
				else:
					print('Account is inactive')
					# Write later something more touchy here 
					return HttpResponse("Your Seller account has been disabled")
			else:
				print('Something went wrong with the input data')
				print(request.POST['username'], request.POST['password'])
				return render(request, 'products/login.html', 
					          {'seller_form': seller_form, 'error_message': "username or password wrong"}
					          )
		else:
			print('Something went really wrong with the input data')
			return render(request, 'products/login.html', 
				           {'error_message': "Please introduce valid data"}
				           )
	else: 
		print('Did not get anything')
		seller_form = LoginForm()
	return render(request, 'products/login.html', 
		           {'seller_form': seller_form})


def loggedIn(request, user=None):
	return render(request, 'products/loggedin.html', {'first_name': user})

def filterSellerItems(request, option):
	if option == 'sold':
	    return
	elif option == 'unsold':
	    return
	else:
	    return HttpResponse("In here you'll soon see the items that you've added to the site!")   

def detailSellerProduct(request, product_id):
	return HttpResponse("You're looking at product %s" % product_id)

def removeProduct(request, product_id):
	return HttpResponse("You're going to remove item %s from your list!" % product_id)

def addProduct(request):
	# Use decorator to ensure that the user is logged in
	# Show formset
	if request.method == 'POST':
		formset = SellerFormSet(request.POST)
		if formset.is_valid():
			cd = formset.cleaned_data
			title = cd.title
			category = cd.category
			description = cd.category
			price = cd.category
			# seller = loggedIn
			# geolocation = seller.address
			# create Product object
			# save Product object
		else:
			pass
	return HttpResponse("You're in the add items page.")




