from django.http import HttpResponse
from .models import Restaurant, User, CustomPasswordResetForm
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone





# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')

# Views for /FoodApp/restaurants
def restaurant_list(request):

    # Get query parameters from the request (user input)
    name_query = request.GET.get('name', '')  # Get the search term for name
    cuisine_query = request.GET.get('cuisine', '')  # Get the search term for cuisine
    sort_by = request.GET.get('sort', 'rating_high_first')  # Default sort by rating
    distance_to = request.GET.get('distance', 'distance_high_first')


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
        'sort_by': sort_by,
        'distance_to': distance_to
    })



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
