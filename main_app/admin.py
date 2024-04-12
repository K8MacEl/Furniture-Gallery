from django.contrib import admin

# Register your models here.
from .models import Furniture_Item, Photo, Cart

admin.site.register(Furniture_Item)
admin.site.register(Photo)
admin.site.register(Cart)