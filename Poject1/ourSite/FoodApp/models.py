from django.db import models
from django import forms


# Create your models here.
#class Cuisine(models.Model):
#    name = models.CharField(max_length=100, unique=True, default="Unknown Name")

#    def __str__(self):
#        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Unknown Name")
    location = models.CharField(max_length=255, default="Unknown Address")  # Address of the restaurant
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # Rating between 0.00 and 5.00

    def __str__(self):
        return self.name


class User(models.Model):
    class User(models.Model):
        username = models.CharField(max_length=70, default="Unknown username", unique=True)
        first_name = models.CharField(max_length=70, default="Unknown first_name", unique=False)
        last_name = models.CharField(max_length=70, default="Unknown last_name", unique=False)
        password = models.CharField(max_length=50, default="password")
        favorites = models.JSONField(default=list, blank =True)

        def __str__(self):
            return self.username

# this is the model that creates the password reset
class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150)
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





