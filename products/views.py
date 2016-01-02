from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.decorators import method_decorator 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.template import RequestContext

from .models import Seller, Product
from .forms import UserForm, SellerForm, LoginForm, ProductForm, FilterForm, ItemsPerPage


class IndexView(generic.ListView):
	template_name = 'products/index.html'
	filter_form = FilterForm
	pagination_form = ItemsPerPage
	filter_form_values = ''
	query_set = ''	

	def get_query_set(self, request):
		print("Estamos en query_set method")
		request_elements = [value for key, value in request.GET.items() if len(value)>0 and key != 'items_per_page']
		query_set = Product.objects
		if len(request_elements)>0:
			filter_form = self.filter_form(request.GET)
			if filter_form.is_valid():
				cd = filter_form.cleaned_data
				if cd['category']:
					category = cd['category']
					query_set = query_set.filter(category=category)
				else: pass
				if cd['min_price']:
					min_price = cd['min_price']
					query_set = query_set.filter(price__gt=min_price)
				else: pass
				if cd['max_price']:
					max_price = cd['max_price']
					query_set = query_set.filter(price__lt=max_price)
				else: pass
				if cd['geolocation']:
					geolocation = cd['geolocation']
					print(geolocation)
					query_set = query_set.filter(seller__address=geolocation)
				else: pass
				print('Query set: ', query_set)
				self.query_set = query_set
				self.filter_form_values = filter_form 
				return query_set, filter_form
		else:
			query_set = query_set.all()
			filter_form = self.filter_form()
			self.query_set = query_set
			self.filter_form_values = filter_form
			return query_set, filter_form
		

	def get(self, request, **kwargs):
		self.get_query_set(request)
		print('Query set: ', self.query_set)

		try:
			items_per_page = kwargs['items_per_page']
			pagination_form = kwargs['pagination_form']
		except KeyError:
			items_per_page = 5
			pagination_form = self.pagination_form()

		paginator = Paginator(self.query_set, items_per_page)
		page = request.GET.get('page') 
		try:
			query_set = paginator.page(page)
		except PageNotAnInteger:
			query_set = paginator.page(1)
		except EmptyPage:
			query_set = paginator.page(paginator.num_pages)	
		except:
			print('Something went really worong...')
			query_set = self.query_set

		return render(request, 'products/index.html', {'products_list': query_set, 
											    			'user': request.user, 
												    		'filter_form': self.filter_form,
												    		'pagination_form': pagination_form}
												    		)


def listing(request):
	pagination_form = ItemsPerPage
	print('Estamos en listing method')
	try: 
		items_per_page = request.GET['items_per_page']
		pagination_form = pagination_form(request.GET)
	except KeyError:
		items_per_page = 5
		pagintion_form = pagination_form()
	print(items_per_page)
	return redirect('/products/' + 'show=' + str(items_per_page) + '/', items_per_page=items_per_page, pagination_form=pagination_form)

		


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

class EditProduct(LoginRequiredMixin, generic.View):
	login_url = "/products/login/"
	product_form = ProductForm

	def get(self, request, product_id):
		product = Product.objects.get(pk=product_id)
		product_form = self.product_form(initial={
												'title': product.title,
												'category': product.category,
												'price': product.price,
												'description': product.description
												})
		return render(request, 'products/edit_product.html', {'product_form': product_form})

	def post(self, request, product_id):
		product = Product.objects.get(pk=product_id)
		product_form = self.product_form(data=request.POST)
		if product_form.is_valid():
			cd = product_form.cleaned_data
			product.title = cd['title']
			product.category = cd['category']
			product.price = cd['price']
			product.description = cd['description']
		product.save()
		return redirect('/products/product/' + product_id)



