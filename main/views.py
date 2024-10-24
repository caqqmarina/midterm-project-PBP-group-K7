from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime

def homepage(request):
    return render(request, 'homepage.html')

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('main:homepage')
    context = {
        'form': form
    }

    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:homepage"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    response = HttpResponseRedirect(reverse('main:homepage'))
    response.delete_cookie('last_login')
    return response


def faculty(request):
    return render(request, 'faculty.html')

@login_required(login_url='/login/')
def user_homepage(request):
    return
# def show_main(request):
#     context = {
#         'group' : 'K7',
#         'class': 'PBP KKI'
#     }

#     return render(request, "main.html", context)




