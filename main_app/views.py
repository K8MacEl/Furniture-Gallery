from django.shortcuts import render, redirect
from allauth.account.signals import user_logged_in
from django.dispatch.dispatcher import receiver
from django.forms.models import model_to_dict
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
from .models import Furniture_Item, Photo, Cart




@receiver(user_logged_in, dispatch_uid="unique")
def user_logged_in_(request, user, **kwargs):
	print(request.user)


def home(request):

	return render(request, 'home.html')


def signup(request):
	error_message = ''
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			# save the user to the database
			user = form.save()  # this adds user to the table in psql
			# login our user
			login(request, user)
			return redirect('index')  # index is the name of the url path
		else:
			error_message = "Invalid signup - try again"
	form = UserCreationForm()
	return render(request, 'registration/signup.html', {
		'error_message': error_message,
		'form': form
	})



def furniture_index(request):
	category = request.GET.get('category')
	if category:
		furniture = Furniture_Item.objects.filter(category=category)
		return render(request, 'furniture/index.html', {
			'furniture': furniture
		})
	else:
		furniture = Furniture_Item.objects.all()
		return render(request, 'furniture/index.html', {
			'furniture': furniture
	})


def furniture_detail(request, furniture_item_id):
	furniture = Furniture_Item.objects.get(id=furniture_item_id)
	return render(request, 'furniture/detail.html', {
		'furniture_item': furniture,
	})

 ## ---create furniture----####



class Furniture_Item_Create(CreateView):
	model = Furniture_Item
	fields = ['name', 'description', 'price', 'category']




class Furniture_Item_Delete(DeleteView):
	model = Furniture_Item
	# define the success_url here because the def get_absolute_url in the models.property
	# redirects to a detail page which doesn't make sense since we deleted it
	success_url = '/furniture'  # redirect to furniture_index path


def add_photo(request, furniture_item_id):
	# photo-file will be the "name" attribute on the <input type="file">
	photo_file = request.FILES.get('photo-file', None)
	if photo_file:
		s3 = boto3.client('s3')
		# need a unique "key" for S3 / needs image file extension too
		key = "furniture_gallery/" + \
		    uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
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




def cart_list(request):
	cart = Cart.objects.get(user=request.user)
	print(cart)
	total_price = sum([item.price * item.quantity for item in cart.furniture_item.all()])
	return render(request, 'main_app/cart_list.html', {'cart': cart, 'total_price': total_price})


def disassoc_item(request, cart_id, furniture_item_id):
	cart = Cart.objects.get(id=cart_id)
	cart.furniture_item.remove(furniture_item_id)
	return redirect('cart_list')






def assoc_item(request, furniture_item_id):
#1 find cart by the user similar to cart = Cart.objects.get(id=cart_id)
#2 if it finds the object:
	cart = Cart.objects.get(user=request.user)
	print(cart.__dict__, "This is request for assoc_item")
	print(cart, "this is cart")
#3 if we found it, now we need to check to see if the item is in the cart
	try:
		item = cart.furniture_item.get(id=furniture_item_id)
#4 if item is in the cart then we want to increase the quantity
#5 if the item is not in the cart, we add the item to the cart make quanity +1
		item.quantity += 1
		item.save()
		print(request, "Item added to your cart")
	except Furniture_Item.DoesNotExist:
			item = cart.furniture_item.add(furniture_item_id)
#6 then we respond to redirect back to the detail page
	return redirect('cart_list')
