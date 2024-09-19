from django.http import HttpResponse
from .models import Restaurant, User
from django.shortcuts import render, redirect



# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

# Views for /FoodApp/restaurants
def restaurant_list(request):

    # Get query parameters from the request (user input)
    name_query = request.GET.get('name', '')  # Get the search term for name
    cuisine_query = request.GET.get('cuisine', '')  # Get the search term for cuisine
    sort_by = request.GET.get('sort', 'rating_high_first')  # Default sort by rating

    # Search capabilities
    restaurants = Restaurant.objects.all()

    # Search by name
    if name_query:
        restaurants = restaurants.filter(name__icontains=name_query)  # Search by name (case insensitive)

    # search by cuisine
    if cuisine_query:
        restaurants = restaurants.filter(cuisine__icontains=cuisine_query)  # Search by cuisine (case insensitive)

    # Sort restaurants by rating (high to low and low to high)
    if sort_by == 'rating_high_first':
        restaurants = restaurants.order_by('-rating')  # Sort by rating (highest first)
    elif sort_by == 'rating_low_first':
        restaurants = restaurants.order_by('rating')  # Sort by rating (lowest first)

    return render(request, 'map.html', {
        'restaurants': restaurants,
        'name_query': name_query,
        'cuisine_query': cuisine_query,
        'sort_by': sort_by
    })



    #View for users


def user_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Basic validation, you can expand this as needed
        if name and password:
            User.objects.create(name=name, password=password)
            return redirect('user_create')  # Redirect after successful form submission
        else:
            error_message = "All fields are required."
            return render(request, 'user_form.html', {'error_message': error_message})

    return render(request, 'user_form.html')

