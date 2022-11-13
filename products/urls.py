from django.urls import path 
from .views import *


urlpatterns = [
	path("", MainPageView.as_view(), name = "homepage"),
	path("shop/", shop_view, name = "shop"),
	path("shop/<slug:slug>", detail_view, name = "detail"),
	path("shop/<slug:slug>/delete", delete_view , name = "delete"),
	path("shop/<slug:slug>/delete_confirm", delete_confirm_view, name = "delete_confirm"),
	path("shop/<slug:slug>/update", update_view , name = "update"),
	
]