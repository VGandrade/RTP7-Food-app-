from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from .models import Restaurant

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def restaurant_list(request):
    # Query all restaurant objects
    restaurants = Restaurant.objects.all()

    # Pass the data to the template
    return render(request, 'restaurants.html', {'restaurants': restaurants})