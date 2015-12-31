from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.decorators import method_decorator 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
#from django.template import RequestContext

from .models import Seller, Product
from .forms import UserForm, SellerForm, LoginForm, ProductForm, FilterForm


class IndexView(generic.ListView):
	template_name = 'products/index.html'
	context_object_name = 'products_list'
	filter_form = FilterForm

	def get_queryset(self):
		return Product.objects.order_by('-created')

	def get(self, request):
		if 'query' in request.GET:
			filters = []
			filter_form = filter_form(request.GET)
			if filter_form.is_valid():
				cd = filter_form.clean_data
				if cd['category']:
					category = cd['category']
				else:
					category = None
				if cd['price']:
					price = cd['price']
				else:
					price = None
				if cd['geolocation']:
					geolocation = cd['geolocation']
				else:
					geolocation = None
				filters.append(category)
				filters.append(price)
				filters.append(geolocation)
			for filt in filters:
				if filt is None:
					filters.remove(filt)
			query_set = Product.objects.get_all()

		else:
			filter_form = filter_form()
			return render(request, 'products/index.html', {'products_list': self.get_queryset, 
															'user': request.user, 
															'filter_form': filter_form})

		


def filterProducts(request, productFilter):
	response = "You're at products which belong to the %s category."
	return HttpResponse(response % productFilter)

class DetailProduct(generic.DetailView):

	def get(self, request, product_id):
		product = Product.objects.get(pk=product_id)
		return render(request, 'products/detail_product.html', {'product': product, 'user': request.user})

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
			return redirect('products:loggedIn', user=user)
	else:
		user_form = UserForm()
		seller_form = SellerForm()
	return render(request, 'products/registration.html', 
		           {'user_form': user_form, 'seller_form': seller_form, 'registered': registered}
		           )

class Login(generic.View):
	seller_form = LoginForm
	template_name = 'products/login.html'

	def get(self, request, *args, **kwargs):
		seller_form = self.seller_form()
		return render(request, self.template_name, {'seller_form': seller_form})

	def post(self, request, *args, **kwargs):
		seller_form = self.seller_form(data=request.POST)
		if seller_form.is_valid():
			cd = seller_form.cleaned_data
			username = cd['username']
			pwd = cd['password']
			seller = authenticate(username=username, password=pwd)
			print('seller is ', seller)
			if seller is not None:
				if seller.is_active:
					print('Account is active')
					login(request, seller)
					print(seller.username)
					return redirect('/products/loggedin/')
				else:
					print('Accunt is inactive')
					# Write later something more touchy here
					return HttpResponse("Your seller account has been disabled")
			else:
				print('Something went wrong with the input data, seller is None')
				print(request.POST['username'], requsest.POST['set_password'])
				return render(request, 'products/login.html', 
								{'seller_form': seller_form, 'error_message': "username or password wrong"}
								)
		else:
			print('Something went really wrong with the input data, data is invalid')
			return render(request, 'products/login.html', 
							{'error_message': "Please introduce valid data"} 
							)

def logout_view(request):
	logout(request)
	return redirect('/products/')


class LoggedIn(LoginRequiredMixin, generic.View):
	login_url = "/products/login/"
	permission_denied_message = 'Please provide a valid username and password'

	def get(self, request):
		seller = Seller.objects.get(user=request.user)
		products_list = seller.product_set.all().order_by('-created')
		return render(request, 'products/loggedin.html', {'user': request.user, 
															'products_list': products_list}
															)

	@method_decorator(login_required(login_url=login_url))
	def dispatch(self, *args, **kwargs):
		return super(LoggedIn, self).dispatch(*args, **kwargs)


@login_required(login_url='/products/login/')
def loggedIn(request):
	seller = Seller.objects.get(username=user.username)
	product_list = seller.product_set.all().order_by('-created')
	return render(request, 'products/loggedin.html', {'user': request.user, 'products_list': products_list})

@login_required
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
	target_product = Product.objects.get(pk=product_id)
	target_product.delete()
	return redirect('/products/loggedin/')

class AddProduct(LoginRequiredMixin, generic.View):
	login_url = "/products/login/"
	product_form = ProductForm
	template_name = 'products/add_product.html'

	def get(self, request, *args, **kwargs):
		product_form = self.product_form()
		return render(request, self.template_name, {'product_form': product_form})

	def post(self, request, *args, **kwargs):
		product_form = self.product_form(data=request.POST)
		if product_form.is_valid():
			product = product_form.save(commit=False)
			product.created = timezone.now()
			seller = Seller.objects.get(user=request.user)
			product.seller = seller
			product.geolocation = product.seller.address
			product.save()
			return redirect('/products/loggedin/')
		else: return render(request, 
							template_name, 
							{'product_form': product_form, 
								'error_message': 'Please introduce valid data'}
							)





