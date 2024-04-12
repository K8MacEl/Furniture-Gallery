from django.shortcuts import render, redirect
from allauth.account.signals import user_logged_in
from django.dispatch.dispatcher import receiver

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
@receiver(user_logged_in, dispatch_uid="unique")
def user_logged_in_(request, user, **kwargs):
	print(request.user)

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
 
class Furniture_Item_Delete(DeleteView):
	model = Furniture_Item 
	# define the success_url here because the def get_absolute_url in the models.property
	# redirects to a detail page which doesn't make sense since we deleted it
	success_url = '/furniture' # redirect to cats_index path

def add_photo(request, furniture_item_id):
	# photo-file will be the "name" attribute on the <input type="file">
	photo_file = request.FILES.get('photo-file', None)
	if photo_file:
		s3 = boto3.client('s3')
		# need a unique "key" for S3 / needs image file extension too
		key = "furniture_gallery/" + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
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


class CartCreate(CreateView):
	model = Cart
	fields = '__all__'


class CartUpdate(UpdateView):
	model = Cart
	fields = '__all__'
	
class CartList(ListView):
	model = Cart
	fields = '__all__'
	
	
 
def disassoc_item(request, cart_id, furniture_item_id):
	cart = Cart.objects.get(id=cart_id)
	cart.furniture.remove(furniture_item_id)
	return redirect('detail',cart_id=cart_id)





# we want to"
# 1 find cart by the user similar to cart = Cart.objects.get(id=cart_id)
#3 if it finds the object:
#4 if we found it, now we need to check to see if the item is in the cart
#5 if item is in the cart then we want to increase the quantity
#6 if the item is not in the cart, we add the item to the cart make quanity +1
#7 then we respond to redirect back to the detail page
def assoc_item(request, furniture_item_id):
	cart = Cart.objects.get(user=request.user)
	print(cart.__dict__, "This is request for assoc_item" )
	# if cart.exists():
	# 	print(cart, "this is cart")
	# if cart has something call .save
	
 	# cart = Cart.objects.get(id=cart_id)
	# cart.furniture.add(furniture_item_id)# adding a row to our through table the one with 2 foriegn keys in sql
	return redirect('cart_list')
