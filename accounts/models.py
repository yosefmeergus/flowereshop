from django.db import models
from django.contrib.auth.models import User
from products.models import Flower


class Profile(models.Model):
	user = models.OneToOneField(User, related_name = "profile", on_delete = models.CASCADE)
	activation_key = models.CharField(max_length = 20)
	key_expires = models.DateTimeField()

	def __str__(self):
		return f"profile:{self.user.username}"


class Favorites(models.Model):
	user = models.OneToOneField(User, related_name = "favorites", on_delete = models.CASCADE)


class FavoritesItem(models.Model):
	favorites = models.ForeignKey(Favorites, related_name = "favorites_items", on_delete = models.CASCADE)
	flower = models.OneToOneField(Flower, related_name = "favorites_item", on_delete = models.CASCADE)


class Cart(models.Model):
	user = models.OneToOneField(User, related_name = "cart", on_delete = models.CASCADE)

	def __str__(self):
		return f"cart:{self.user.username}"


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, related_name = "cart_items", on_delete = models.CASCADE)
	quantity = models.IntegerField(default = 1)
	flower = models.OneToOneField(Flower, related_name = "cart_item", on_delete = models.CASCADE)
	price = models.FloatField(blank = True)
	
	def __str__(self):
		return f"title: {self.flower.title}-quantity:{self.quantity}"

	def change_quantity(self, change):
		self.quantity += change
		self.price = round(self.flower.cost*self.quantity, 2)
		self.save()