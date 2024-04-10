from django.shortcuts import render

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