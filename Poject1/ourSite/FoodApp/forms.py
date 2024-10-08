from django import forms
from .models import Restaurant

class ReviewForm(forms.Form):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), empty_label="Select a Restaurant")
    review = forms.CharField(widget=forms.Textarea)
