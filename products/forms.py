from django import forms
from .models import Flower


class CreateFlowerForm(forms.ModelForm):
	class Meta:
		model = Flower
		fields = ["title", "description", "image", "cost"]
