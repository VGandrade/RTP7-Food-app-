from django.http import HttpResponse
from .models import Restaurant, User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User



# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

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



    #View for userss


def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        # Basic validation, you can expand this as needed
        if username and password and first_name and last_name:
            user = User.objects.create(username=username,first_name= first_name,last_name= last_name)
            user.set_password(password)
            user.save()

            return redirect('login')  # Redirect after successful form submission
        else:
            error_message = "All fields are required."
            return render(request, 'user_form.html', {'error_message': error_message})

    return render(request, 'user_form.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('user_list')  # Redirect to user list or another appropriate page
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


