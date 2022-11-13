from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Profile, CartItem, Cart, Favorites, FavoritesItem
from products.forms import CreateFlowerForm
from products.models import Flower
from django.contrib import messages
from django.template import loader
from django.core.mail import EmailMessage
from django.utils import timezone
from django.http import HttpResponseRedirect
import random


def sign_in_view(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username = username, password = password)
		if user is not None: 
			login(request, user) 
			return redirect("homepage")	
		else:
			messages.error(request, "your password or username is incorrect")
	return render(request, "accounts/sign_in.html")


def sign_out_view(request):
	logout(request)
	return redirect("homepage")


def sign_up_view(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			email = form.cleaned_data.get("email")
			password = form.cleaned_data.get("password1")
			template = loader.get_template("accounts/email.html")	
			chars = "abcdefghijklmnopqrstuvwxynz0123456789"
			code = ""
			for x in range(20):
				code += random.choice(chars)
			ctx = {
				"username": username,
				"link": f"http://127.0.0.1:8000/accounts/activate/{code}",
			}
			message = template.render(ctx) 
			mail = EmailMessage("Welcome to Flower shop!", message, to = [email])
			mail.content_subtype = "html" 									
			mail.send() 
			form.save(username, email, password, code) 
			return redirect("email_sent") 
	else:                                
		form = SignUpForm()
	ctx = {
		"form": form
	}
	return render(request, "accounts/sign_up.html", ctx)


def profile_view(request):
	if request.method == "POST":
		form = CreateFlowerForm(request.POST, request.FILES)
		if form.is_valid():
			title = form.cleaned_data.get("title")
			description = form.cleaned_data.get("description")
			image = form.cleaned_data.get("image")
			cost = form.cleaned_data.get("cost")
			flower = Flower.objects.create(
					title = title,
					description = description,
					image = image,
					cost = cost,
					owner = request.user
				)
			flower.save()
			form = CreateFlowerForm()
	else:
		form = CreateFlowerForm()
	ctx = {
		"form": form,
		"flowers": Flower.objects.filter(owner = request.user)
	}
	return render(request, "accounts/profile.html", ctx)


def email_sent_view(request):
	ctx = {}
	return render(request, "accounts/email_sent.html", ctx)


def activate_view(request, code):
	profile = Profile.objects.get(activation_key = code)
	if not profile.user.is_active:
		if timezone.now()<profile.key_expires:
			profile.user.is_active = True
			profile.user.save()
		else:
			return redirect("sign_up")
	return redirect("sign_in")


def favorites_view(request):
	favorites = request.user.favorites.favorites_items.all()
	flowers = []
	for favorite in favorites:
		favorite.flower.is_favorite = True
		flowers.append(favorite.flower)
	ctx = {
		"flowers":flowers,
	}
	return render(request, "accounts/favorites.html", ctx)


def handle_favorites_view(request, slug):
	flower = Flower.objects.get(slug = slug)
	favorites = request.user.favorites.favorites_items.filter(flower = flower)
	if len(favorites)>0:
		favorite = request.user.favorites.favorites_items.get(flower = flower)
		favorite.delete() 
	else: 
		favorite = FavoritesItem.objects.create(favorites = request.user.favorites, flower = flower)
		favorite.save() 
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))	


def cart_view(request):
	total = 0
	cart_items = request.user.cart.cart_items.all()
	for x in cart_items:
		total += x.price
	ctx = {
		"cart_items":cart_items,
		"total":round(total, 2),
	}
	return render(request, "accounts/cart.html", ctx)


def add_to_cart_view(request, slug):
	flower = Flower.objects.get(slug = slug)
	cart = Cart.objects.get(user = request.user)
	if len(cart.cart_items.filter(flower = flower)) == 0:
		cart_item = CartItem.objects.create(flower = flower, cart = cart, price = flower.cost)
		cart_item.save()
	else:
		cart_item = cart.cart_items.get(flower = flower)
		cart_item.change_quantity(1)
	return redirect("shop") 


def increase_quantity_view(request, id):
	cart_item = request.user.cart.cart_items.get(id = id)
	cart_item.change_quantity(1)
	return redirect("cart")


def decrease_quantity_view(request, id):
	cart_item = request.user.cart.cart_items.get(id = id)
	if cart_item.quantity > 1:
		cart_item.change_quantity(-1)
	else:
		cart_item.delete()
	return redirect("cart")
