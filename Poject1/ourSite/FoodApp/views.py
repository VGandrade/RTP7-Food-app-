from django.http import HttpResponse
from .models import Restaurant, User, CustomPasswordResetForm, Review
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
import json
import requests
from django.http import JsonResponse

# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

# Views for /FoodApp/restaurants
def restaurant_list(request):
    api_key = 'AIzaSyD4oBoretFq5JNK1Zzo2gxk5rSedxmtjiw'  # Replace with your actual Google Places API key
    api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Get query parameters from the request (user input)
    name_query = request.GET.get('name', '')  # Get the search term for name
    sort_by = request.GET.get('sort', 'rating_high_first')  # Default sort by rating

    params = {
        'location': '33.7490,-84.3880',  # Atlanta, GA coordinates
        'radius': 5000,  # Radius in meters (5km)
        'type': 'restaurant',
        'keyword': name_query,
        'key': api_key
    }

    response = requests.get(api_url, params=params)
    restaurant_data_from_api = response.json().get('results', [])

    # Save restaurant data to the database and gather the list of restaurants
    all_restaurants = []
    for restaurant in restaurant_data_from_api:
        name = restaurant.get('name')
        location = restaurant['geometry']['location']  # Use geometry for location
        lat = location['lat']
        lng = location['lng']
        rating = restaurant.get('rating', 0)

        distance = 0  # Calculate distance if needed

        # Save restaurant to the database
        save_restaurant_to_db(name, f"{lat},{lng}", rating, distance)

        # Prepare restaurant data for map display
        all_restaurants.append({
            'name': name,
            'location': {'lat': lat, 'lng': lng},
            'rating': rating,
            'distance': distance
        })

    return render(request, 'map.html', {
        'restaurants': all_restaurants,  # Pass the list of restaurants to the template
    })


def save_restaurant_to_db(name, location, rating, distance):
    if not Restaurant.objects.filter(name=name, location=location).exists():
        Restaurant.objects.create(name=name, location=location, rating=rating, distance=distance)

    #View for userss


def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('usern')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        if username and password and first_name and last_name:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                error_message = "Username already exists. Please choose a different one."
                return render(request, 'user_form_test.html', {'error_message': error_message})

        # Basic validation, you can expand this as needed
        if username and password and first_name and last_name:
            user = User.objects.create(username=username,first_name= first_name,last_name= last_name)
            user.set_password(password)
            user.save()


            return redirect('login')  # Redirect after successful form submission
        else:
            error_message = "All fields are required."
            return render(request, 'user_form_test.html', {'error_message': error_message})

    return render(request, 'user_form_test.html')

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('usern')
        password = request.POST.get('password')

        # Authenticate the user
        user = User.objects.get(username=username)

        if (check_password(password, user.password)) :
            # Login the user
            login(request, user)
            return redirect('restaurant_list')  # Redirect to user list or another appropriate page
        else:
            error_message = "Invalid username or password."
            return render(request, 'newLogin.html', {'error_message': error_message})

    return render(request, 'newLogin.html')



# View for user profile
def user_profile(request, usern):
    user = User.objects.get(username=usern)
    print("profile " + user.username)
    for x in range(len(user.favorites)):
        print(user.favorites[x])
    return render(request, 'user_profile.html', {'user_profile': user})


def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['usern']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            new_password = form.cleaned_data['new_password']

            try:
                # Find the user with the given username, first name, and last name
                user = User.objects.get(username =username, first_name=first_name, last_name=last_name)

                # Update the user's password
                user.set_password(new_password)
                user.save()

                # Provide feedback and redirect
                messages.success(request, 'Password successfully reset. You can now log in with your new password.')
                return redirect('login')  # Redirect to login page after password reset

            except User.DoesNotExist:
                # If the user does not exist, show an error
                messages.error(request, 'No user found with the provided details.')

    else:
        form = CustomPasswordResetForm()

    return render(request, 'custom_password_reset.html', {'form': form})

def add_favorite(request, username):
    user = User.objects.get(username=username)
    restaurant = request.POST.get('restaurant')
    print(len(user.favorites))
    user.add_favorite(restaurant)
    for x in range(len(user.favorites)):
        print(user.favorites[x])
    return redirect('restaurant_list')

# @login_required
# def leave_review(request):
#     if request.method == "POST":
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             restaurant_name = form.cleaned_data['restaurant']
#             try:
#                 restaurant = Restaurant.objects.get(name=restaurant_name)
#             except Restaurant.DoesNotExist:
#                 messages.error(request, f"No restaurant found with the name {restaurant_name}")
#                 return redirect('leave_review')  # Redirect back to the review form if no restaurant is found
#
#             review_content = form.cleaned_data['review']
#             review = Review(user=request.user, restaurant=restaurant, content=review_content)
#             review.save()
#             messages.success(request, 'Your review has been posted.')
#             return redirect('review_list')  # Replace with the appropriate view for listing reviews
#     else:
#         form = ReviewForm()
#
#     return render(request, 'leave_review.html', {'form': form})
#
# def review_list(request):
#     reviews = Review.objects.all().order_by('-created_at')
#     return render(request, 'review_list.html', {'reviews': reviews})


@login_required
def leave_and_list_reviews(request):
    reviews = None  # Initialize reviews variable

    # Handle review submission
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            restaurant = form.cleaned_data['restaurant']
            review_content = form.cleaned_data['review']
            review = Review(user=request.user, restaurant=restaurant, content=review_content)
            review.save()
            messages.success(request, 'Your review has been posted.')
            return redirect('leave_and_list_reviews')  # Reload the page after form submission
    else:
        form = ReviewForm()

    # Handle displaying reviews for a selected restaurant
    if 'restaurant_filter' in request.GET:
        restaurant_name = request.GET['restaurant_filter']
        try:
            selected_restaurant = Restaurant.objects.get(name=restaurant_name)
            reviews = Review.objects.filter(restaurant=selected_restaurant)
        except Restaurant.DoesNotExist:
            messages.error(request, f"No restaurant found with the name {restaurant_name}")
            reviews = None

    restaurants = Restaurant.objects.all()  # For the dropdown selection

    return render(request, 'leave_and_list_reviews.html', {
        'form': form,
        'reviews': reviews,
        'restaurants': restaurants,
    })

def save_restaurant(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract restaurant details from the request
        name = data.get('name', 'Unknown Name')
        location = data.get('location', 'Unknown Address')
        rating = data.get('rating', 0.00)
        distance = data.get('distance', 0.00)

        # Check if restaurant already exists
        restaurant, created = Restaurant.objects.get_or_create(
            name=name,
            defaults={'location': location, 'rating': rating, 'distance': distance}
        )

        # Update restaurant details if not created
        if not created:
            restaurant.location = location
            restaurant.rating = rating
            restaurant.distance = distance
            restaurant.save()

        return JsonResponse({'message': 'Restaurant saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
