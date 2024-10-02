from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
import json

from django.conf import settings


# Create your models here.
# class Cuisine(models.Model):
#    name = models.CharField(max_length=100, unique=True, default="Unknown Name")

#    def __str__(self):
#        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Unknown Name")
    location = models.CharField(max_length=255, default="Unknown Address")  # Address of the restaurant
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # Rating between 0.00 and 5.00
    distance = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Distances from user to restaurants

    def __str__(self):
        return self.name



class User(AbstractUser):
    #    usern = models.CharField(max_length=70, default="Unknown username", unique=True)
    #    first_name = models.CharField(max_length=70, default="Unknown first_name", unique=False)
    #    last_name = models.CharField(max_length=70, default="Unknown last_name", unique=False)
    #    password = models.CharField(max_length=256, default="password")
    #    favorites = models.JSONField(default=list, blank =True)
    #    last_login = models.DateTimeField(null=True,blank=True)
    username = models.CharField(max_length=70, default="Unknown_username", unique=True)
    favorites = models.JSONField(default=list, blank=True)

    def add_favorite(self, restaurant):
        if restaurant not in self.favorites:
            self.favorites.append(restaurant)
            self.save()

    def remove_favorite(self, restaurant):
        if restaurant in self.favorites:
            self.favorites.remove(restaurant)
            self.save()

    def __str__(self):
        return self.username


# this is the model that creates the password reset
class CustomPasswordResetForm(forms.Form):
    usern = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who left the review
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # The restaurant being reviewed
    content = models.TextField()  # The review content
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # User's rating for the restaurant
    created_at = models.DateTimeField(auto_now_add=True)  # When the review was left

    def __str__(self):
        return f"Review by {self.user.username} for {self.restaurant.name}"





