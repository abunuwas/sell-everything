from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

def index(request):
	return HttpResponse("Hello, world. You're at the polls index")

def filterProducts(request, productFilter):
	response = "You're at products which belong to the %s category."
	return HttpResponse(response % productFilter)

def detailProduct(request, product_id):
	return HttpResponse("You've purchased product %s" % product_id)

def buyProduct(request, product_id):
	return HttpResponse("You've purchased product %s" % product_id)

def register(request):
	if request.method == 'POST':
		formset = SellerFormSet(request.POST)
		if formset.is_valid():
			cd = formset.cleaned_data
			name = cd.name
			address = cd.address
			email = cd.email
			pwd = cd.password
			# create Seller object
			# save Seller object
		else:
			pass
	return HttpResponse("You're in the register page.")

def logIn(request):
	if request.method == 'POST':
		formset = SellerFormSet(request.POST)
		if formset.is_valid():
			cd = formset.cleaned_data
			name = cd.name
			address = cd.address
			email = cd.email
			pwd = cd.password
		else:
			return HttpResponseRedirect('products/loggedin/')
    # Show a view with the list of items uploaded by hte user and two options: 
    # list unsold or sold items and add items 
	else: return HttpResponse("You're in the login page!")

def loggedIn(request):
	return HttpResponse("Hi %s!" % 'joe')

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




