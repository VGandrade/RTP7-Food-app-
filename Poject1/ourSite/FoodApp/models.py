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
    cuisine = models.CharField(max_length=100, default="Unknown Cuisine") # Cuisine of the restaurant
    phonenum = models.CharField(max_length=15, null=True, blank=True) # phone number
    website = models.CharField(max_length=30, default="Unknown Website") # website for the restaurant

    def __str__(self):
        return f"{self.name} restaurant serving {self.cuisine} cuisine at {self.location} with rating {self.rating}. To contact the restaurant, call at {self.phonenum} or visit their website at {self.website}"
