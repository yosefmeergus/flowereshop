from django.urls import path 
from .views import *


urlpatterns = [
	path("signin/", sign_in_view, name = "sign_in"),
	path("signout/", sign_out_view, name = "sign_out"),
	path("signup/", sign_up_view, name = "sign_up"),
	path("profile/", profile_view, name = "profile"),
	path("email_sent/", email_sent_view, name = "email_sent"),
	path("cart/", cart_view, name = "cart"),
	path("activate/<str:code>", activate_view, name = "activate"),
	path("cart/add/<slug:slug>", add_to_cart_view, name = "add_to_cart"),
	path("cart/increase/<int:id>", increase_quantity_view, name = "increase"),
	path("cart/decrease/<int:id>", decrease_quantity_view, name = "decrease"),
	path("favorites/", favorites_view, name = "favorites"),
	path("favorites/handle/<slug:slug>", handle_favorites_view, name = "handle_favorites"),
]
