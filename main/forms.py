from django import forms
from .models import Faculty, Canteen, Stall, Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class FacultyForm(forms.ModelForm):
    colors = forms.CharField(help_text="Enter colors separated by commas (e.g., 'red' or 'red,blue' or 'red,blue,green')")
    
    class Meta:
        model = Faculty
        fields = ['name', 'nickname', 'colors', 'image']

class CanteenForm(forms.ModelForm):
    class Meta:
        model = Canteen
        fields = ['name', 'faculty', 'image', 'price']

class StallForm(forms.ModelForm):
    class Meta:
        model = Stall
        fields = ['name', 'cuisine', 'canteen']  

    cuisine = forms.ChoiceField(choices=Stall.CUISINE_CHOICES, label="Cuisine Type")
    canteen = forms.ModelChoiceField(queryset=Canteen.objects.all(), label="Canteen")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stall']

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)