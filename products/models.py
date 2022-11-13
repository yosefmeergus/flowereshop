from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Flower(models.Model):
	title = models.CharField(max_length = 50)
	description = models.TextField(max_length = 500)
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	slug = models.SlugField(unique = True)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	image = models.ImageField()	
	cost = models.FloatField()

	def __str__(self):
		return f"title: {self.title}-cost:{self.cost}"

	def save(self, *args, **kwargs):
		slug = slugify(self.title)
		answer = Flower.objects.filter(slug = slug)
		if answer.exists():
			slug = f"{slug}-{answer.first().id}"
		self.slug = slug
		return super().save(*args, **kwargs)

