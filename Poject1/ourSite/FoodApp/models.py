from django.db import models


# Create your models here.
#class Cuisine(models.Model):
#    name = models.CharField(max_length=100, unique=True, default="Unknown Name")

#    def __str__(self):
#        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Unknown Name")
    location = models.CharField(max_length=255, default="Unknown Address")  # Address of the restaurant
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # Rating between 0.00 and 10.00
    cuisine = models.CharField(max_length=100, default="Unknown Cuisine")

    def __str__(self):
        return f"{self.name} restaurant serving {self.cuisine} cuisine at {self.location} with rating {self.rating}"

class User(models.Model):
    class User(models.Model):
        username = models.CharField(max_length=70, default="Unknown username", unique=True)
        first_name = models.CharField(max_length=70, default="Unknown first_name", unique=False)
        last_name = models.CharField(max_length=70, default="Unknown last_name", unique=False)
        password = models.CharField(max_length=50, default="password")

        def __str__(self):
            return self.username



