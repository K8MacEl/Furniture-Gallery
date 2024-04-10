from django.shortcuts import render

# Login
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Authorization
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def furniture_index(request):

	# tell the model to find all the rows in the cats table!
	furniture = Furniture.objects.all()
	return render(request, 'furniture/index.html', {
		'furniture': furniture
		# 'furniture' becomes a variable name in 'furniture/index.html'
		# just like express
		# res.render('furniture/index', {'furniture': furniture})
	})