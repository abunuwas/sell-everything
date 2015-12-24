from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^filter/(?P<productFilter>\w+)/$', views.filterProducts, name='filterProducts'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.detailProduct, name='detailProduct'),
    url(r'^buy/(?P<product_id>[0-9]+)/$', views.buyProduct, name='buyProduct'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.logIn, name='logIn'),
    url(r'^loggedin/$', views.loggedIn, name='loggedIn'),
    url(r'^loggedin/items/$', views.register, name='register'),
    url(r'^loggedin/filter/(?P<productFilter>\w+)/$', views.filterSellerItems, name='filterSellerItems'),
    url(r'^loggedin/filter/(?P<product_id>[0-9]+)/$', views.detailSellerProduct, name='detailSellerProduct'),
    url(r'^loggedin/addproduct/$', views.addProduct, name='addProduct'),
    ]