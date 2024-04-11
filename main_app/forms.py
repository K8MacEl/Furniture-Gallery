from django.forms import ModelForm
from .models import Furniture_Item

class FurnitureForm(ModelForm):
    class Meta:
        model = Furniture_Item
        fields = ['category']
