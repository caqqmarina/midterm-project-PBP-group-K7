from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product, Faculty, Canteen, Stall
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import FacultyForm, CanteenForm, StallForm, ProductForm
import json
import datetime

def is_admin(user):
    return user.is_staff

def homepage(request):
    # Sample data for demonstration purposes
    bites = [
        {
            'title': 'Faculty of Science',
            'description': 'Explore the best canteen at the Faculty of Science...',
            'image_url': 'images/makaravokasi.png',
            # 'link': '/faculty/science'
        },
        {
            'title': 'Faculty of Arts',
            'description': 'Taste the unique dishes at the Faculty of Arts...',
            'image_url': 'images/faculty_arts.png',
            # 'link': '/faculty/arts'
        },
        {
            'title': 'Faculty of Engineering',
            'description': 'Find out the top-rated food at the Faculty of Engineering...',
            'image_url': 'images/faculty_engineering.png',
            # 'link': '/faculty/engineering'
        },
        {
            'title': 'Faculty of Computer Science',
            'description': 'Explore the best canteen at the Faculty of Science...',
            'image_url': 'images/makaravokasi.png',
            # 'link': '/faculty/science'
        },
        {
            'title': 'Library',
            'description': 'Taste the unique dishes at the Faculty of Arts...',
            'image_url': 'images/faculty_arts.png',
            # 'link': '/faculty/arts'
        },
        {
            'title': 'Faculty of Politics and Social Studies',
            'description': 'Find out the top-rated food at the Faculty of Engineering...',
            'image_url': 'images/faculty_engineering.png',
            # 'link': '/faculty/engineering'
        },
    ]
    context = {
        'bites': bites,
        'username' : request.user.username
    }
    return render(request, 'homepage.html', context)


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('main:login')
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
    data = Canteen.objects.all()
    context = {'data': data}
    return render(request, 'faculty.html', context)

def canteen(request, name):
    canteen = Canteen.objects.get(name=name)

    data = Stall.objects.filter(canteen=canteen)

    context = {'data': data, 'faculty_name': name}
    return render(request, 'canteen.html', context)

def stall(request, canteen_name, stall_name):
    canteen = get_object_or_404(Canteen, name=canteen_name)
    stall = get_object_or_404(Stall, canteen=canteen, name=stall_name)
    products = Product.objects.filter(stall=stall)

    context = {
        'products': products,
        'canteen_name': canteen_name,
        'stall_name': stall_name
    }
    return render(request, 'stall.html', context)



@login_required(login_url='/login/')
def user_homepage(request):
    return

@user_passes_test(is_admin, login_url='/login/')
@login_required
def add_faculty_and_canteen(request):
    faculty_form = FacultyForm(request.POST or None)
    canteen_form = CanteenForm(request.POST or None)
    
    if request.method == 'POST':
        if faculty_form.is_valid() and canteen_form.is_valid():
            # Get or create the faculty
            faculty, created = Faculty.objects.get_or_create(
                name=faculty_form.cleaned_data['name'],
                defaults={
                    'nickname': faculty_form.cleaned_data['nickname'],
                    'name_css_class': faculty_form.cleaned_data['name_css_class'],
                    'image': faculty_form.cleaned_data['image']
                }
            )
            
            # If faculty was created, link canteen to it
            if created:
                canteen = canteen_form.save(commit=False)
                canteen.faculty = faculty  # Link the canteen to the newly created faculty
                canteen.save()
                messages.success(request, f"Faculty '{faculty.name}' and Canteen '{canteen.name}' created successfully!")
            else:
                messages.error(request, f"Faculty '{faculty.name}' already exists.")
            
            return redirect('main:faculty')  # Redirect to the faculty page or any other page

    context = {
        'faculty_form': faculty_form,
        'canteen_form': canteen_form
    }
    return render(request, 'add_faculty_and_canteen.html', context)

@user_passes_test(is_admin, login_url='/login/')
def add_canteen(request):
    if request.method == 'POST':
        form = CanteenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:faculty')  # Adjust the redirect as needed
    else:
        form = CanteenForm()
    return render(request, 'add_canteen.html', {'form': form})

@user_passes_test(is_admin, login_url='/login/')
def add_stall(request):
    if request.method == 'POST':
        form = StallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:stall_list')  # Adjust the redirect as needed
    else:
        form = StallForm()
    return render(request, 'add_stall.html', {'form': form})

@user_passes_test(is_admin, login_url='/login/')
def add_product(request, stall_id=None):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:')  # Adjust as needed
    else:
        form = ProductForm(initial={'stall': stall_id} if stall_id else None)

    context = {
        'form': form,
        'stall_id': stall_id,
    }
    return render(request, 'add_product.html', context)


@user_passes_test(is_admin, login_url='/login/')
@login_required
def delete_faculty(request, faculty_id):
    if request.method == 'POST':
        faculty = get_object_or_404(Faculty, id=faculty_id)  # Match against 'id' field
        faculty.delete()
        return redirect('main:faculty')  # Redirect to the faculty listing page

def show_json(request):
    faculties = Faculty.objects.all()
    canteens = Canteen.objects.all()
    stalls = Stall.objects.all()
    products = Product.objects.all()

    data = {
        'faculties': json.loads(serializers.serialize('json', faculties)),
        'canteens': json.loads(serializers.serialize('json', canteens)),
        'stalls': json.loads(serializers.serialize('json', stalls)),
        'products': json.loads(serializers.serialize('json', products)),
    }

    pretty_data = json.dumps(data, indent=4)

    return HttpResponse(pretty_data, content_type='application/json')