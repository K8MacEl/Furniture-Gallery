from django.shortcuts import render
def home(request):
    return render(request, 'home.html')


# Login
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Authorization
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def furniture_index(request):


