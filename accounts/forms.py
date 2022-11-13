from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Cart, Favorites
import datetime as dti



class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def save(self, username, email, password, activation_key):
		user = User.objects.create_user(username, email, password)
		time = dti.datetime.strftime(dti.datetime.now()+dti.timedelta(hours = 6), "%Y-%m-%d %H:%M:%S")
		user.is_active = False
		profile = Profile.objects.create(user = user, activation_key = activation_key, key_expires = time)
		cart = Cart.objects.create(user = user)			
		favorites = Favorites.objects.create(user = user)
		profile.save()
		cart.save()
		user.save()
		favorites.save()
