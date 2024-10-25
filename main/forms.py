from django import forms
from .models import Faculty, Canteen, Stall, Product

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'nickname', 'name_css_class', 'image']

class CanteenForm(forms.ModelForm):
    class Meta:
        model = Canteen
        fields = ['name', 'faculty', 'image', 'price']

class StallForm(forms.ModelForm):
    class Meta:
        model = Stall
        fields = ['name', 'canteen', 'cuisine']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stall']