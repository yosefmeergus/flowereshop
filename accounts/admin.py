from django.contrib import admin
from .models import *


admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorites)
admin.site.register(FavoritesItem)