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
from .models import Furniture_Item

def home(request):
	furniture = Furniture_Item.objects.all()

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
	furniture = Furniture_Item.objects.filter(category=request.category)
	return render(request, 'furniture/index.html', {
# user filter method like we did in the cat but category
# when click on the link use query string of category for index
		'furniture': furniture
	})
	
def furniture_detail(request, furniture_id):
	furniture = Furniture_Item.objects.get(id=furniture_id)
 
 ##---create furniture----####
 
 ## AAU (ADMIN ONLY) I want to create new furniture item
# class FurnitureCreate(LoginRequiredMixin, CreateView):
# 	model = Furniture_Item
# 	fields = ['name', 'description', 'price', 'category'],
# 	def form_valid(self, form):
# 		form.instance.user = self.request.user
# 		return super().form_valid(form)
 
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
 