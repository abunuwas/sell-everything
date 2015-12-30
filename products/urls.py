from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

app_name = 'products'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^filter/(?P<productFilter>\w+)/$', views.filterProducts, name='filterProducts'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.detailProduct, name='detailProduct'),
    url(r'^buy/(?P<product_id>[0-9]+)/$', views.buyProduct, name='buyProduct'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.Login.as_view(), name='logIn'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^loggedin/$', views.LoggedIn.as_view(), name='loggedIn'),
    url(r'^loggedin/filter/(?P<productFilter>\w+)/$', views.filterSellerItems, name='filterSellerItems'),
    url(r'^loggedin/filter/(?P<product_id>[0-9]+)/$', views.detailSellerProduct, name='detailSellerProduct'),
    url(r'^loggedin/addproduct/$', views.AddProduct.as_view(), name='addProduct'),
    ]