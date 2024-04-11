from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DeleteView

# Login
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Authorization
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


import uuid
import boto3
import os
#---confirm with Dean this model is done then migrate
from .models import Furniture_Item, Photo, Cart

# furniture = [
# 	{'name':'Blue chair', 'description': 'Blue LazyBoy', 'price':'500.00', 'category':'chair'},
# 	{'name':'Dining table', 'description': 'Oak Dining Table', 'price':'1000.00', 'category':'table'},
#  	{'name':'Canopy Bed', 'description': 'Black metal canopy bed', 'price':'250.00', 'category':'bed'},
# 	{'name':'Sectional', 'description': 'Leather Sectional', 'price':'1500,00', 'category':'sofa'}
# ]

def home(request):
	# furniture = furniture.objects.all()

	return render(request, 'home.html')

def signup(request):
	error_message = ''
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			# save the user to the database
			user = form.save() # this adds user to the table in psql
			# login our user
			login(request, user)
			return redirect('index') # index is the name of the url path
		else:
			error_message = "Invalid signup - try again"
	form = UserCreationForm()
	return render(request, 'registration/signup.html', {
		'error_message': error_message,
		'form': form
	})

#----WILL NEED TO ADD FILTER METHOD HERE----#
def furniture_index(request):

	# tell the model to find all the rows in the cats table!
	# cats = Cat.objects.all()
	# Only grab the logged in users cats
	furniture = Furniture_Item.objects.all()
	return render(request, 'furniture/index.html', {
		'furniture': furniture
		# 'cats' becomes a variable name in 'cats/index.html'
		# just like express
		# res.render('cats/index', {'cats': cats})
	})
	
def furniture_detail(request, furniture_item_id):
	furniture = Furniture_Item.objects.get(id=furniture_item_id)
	return render(request, 'furniture/detail.html', {
		'furniture_item': furniture,
	})
 
 ##---create furniture----####
 
 ## AAU (ADMIN ONLY) I want to create new furniture item


class Furniture_Item_Create(CreateView):
	model = Furniture_Item
	fields = ['name', 'description', 'price', 'category']

	# def form_valid(self, form):
	# 	#uncomment this when signup is fully working 
	# 	form.instance.user = self.request.user
	# 	return super().form_valid(form)

def add_photo(request, furniture_item_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to furniture_id or cat (if you have a furniture object)
            Photo.objects.create(url=url, furniture_item_id=furniture_item_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', furniture_item_id=furniture_item_id)
 
 ##---edit/update furniture---##
 
 ##--AAU (ADMIN ONLY) I want to edit furniture


# class FurnitureUpdate(LoginRequiredMixin, UpdateView):
#     model = Furniture_Item
#     fields = ['name', 'description', 'price', 'category'], 
 ##---delete furniture---##
 
 ##--AAU (ADMIN ONLY) I want to delete furniture
 
# class FurnitureDelete(LoginRequiredMixin, DeleteView):
#     model = Furniture_Item
#     success_url = '/furniture' # redirect to furniture_index path 
 
  ##-----remaining functions to create here-----##
  
 ###-----add_to_cart----###
 ##---AAU I want to add furninture to cart---## 
 
 ##----remove_from_cart----##
 ###----AAU I want to remove furniture from from---##
 
