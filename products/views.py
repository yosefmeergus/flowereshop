from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Flower 
from .forms import CreateFlowerForm


class MainPageView(TemplateView):
	template_name = "products/main.html"


def shop_view(request):
	search = request.GET.get("search")
	price = request.GET.get("price")
	if price is None or price == "asc":
		order = "cost"
	else:
		order = "-cost"
	if search is not None and len(search) > 0:
		flowers = Flower.objects.filter(title__icontains = search).order_by(order)
	else:
		flowers = Flower.objects.all().order_by(order)
	for flower in flowers:
		filteer = request.user.favorites.favorites_items.filter(flower = flower)
		if len(filteer) > 0:
			flower.is_favorite = True
		else:
			flower.is_favorite = False
	ctx = {
		"flowers":flowers,
		"search":search,
	}
	return render(request, "products/shop.html", ctx)


def detail_view(request, slug):
	flower = get_object_or_404(Flower, slug = slug)
	ctx = {
		"flower":flower,
	}
	return render(request, "products/detail.html", ctx)


def delete_view(request, slug):
	ctx = {
		"flower":get_object_or_404(Flower, slug = slug)
	}
	return render(request, "products/delete.html", ctx)


def delete_confirm_view(request, slug):
	flower = get_object_or_404(Flower, slug = slug)
	flower.delete()
	return redirect("profile")


def update_view(request, slug):
	flower = get_object_or_404(Flower, slug = slug)
	form = CreateFlowerForm( instance = flower)
	if request.method == "POST":
		form = CreateFlowerForm( request.POST, instance = flower)
		if form.is_valid():
			form.save()
			return redirect("profile")
	ctx = {
		"form":form
	}
	return render(request, "products/update.html", ctx)
