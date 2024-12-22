from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product, Faculty, Canteen, Stall, ProductReview, FavoriteProduct, User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import FacultyForm, CanteenForm, StallForm, ProductForm
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
import datetime
from django.utils.timezone import now
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stall_id = data.get("stall")
            stall = Stall.objects.get(pk=stall_id)  # Get the Stall object by its ID
            
            new_product = Product.objects.create(
                name=data["name"],
                price=float(data["price"]),
                stall=stall,
            )
            return JsonResponse({"status": "success", "product_id": new_product.id}, status=200)
        except Stall.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid stall ID"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid HTTP method"}, status=405)

@csrf_exempt
def edit_product_flutter(request, id):
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body.decode('utf-8'))
            
            # Fetch the product to edit
            product = get_object_or_404(Product, pk=id)
            
            # Update product fields with the new data
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.stock = data.get('stock', product.stock)
            
            # Save the updated product
            product.save()
            
            return JsonResponse({'status': 'success', 'message': 'Product updated successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method. Use POST.'})

@csrf_exempt
def delete_product_flutter(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid HTTP method"}, status=405)

def is_admin(user):
    return user.is_staff

def homepage(request):
    faculties = Faculty.objects.all()
    bites = []

    for faculty in faculties:
        canteens = Canteen.objects.filter(faculty=faculty)
        for canteen in canteens:
            bites.append({
                'title': faculty.name,
                'description': f'Explore the best canteen at the {faculty.name}...',
                'image_url': faculty.image if faculty.image else 'images/default.png',
                'link': f'/canteen/{canteen.name}'
            })

    context = {
        'bites': bites,
        'username': request.user.username
    }
    return render(request, 'homepage.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    response = HttpResponseRedirect(reverse('main:homepage'))
    response.delete_cookie('last_login')
    return response

def login_and_register(request):
    form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()

    if request.method == 'POST':
        if 'signUp' in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('main:homepage')
            else:
                messages.error(request, 'Registration failed. Please correct the errors below.')
        elif 'signIn' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('main:homepage')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Login failed. Please correct the errors below.')

    return render(request, 'login_and_register.html', {'form': form, 'login_form': login_form})


def faculty(request):
    data = Canteen.objects.all()
    context = {'data': data}
    return render(request, 'faculty.html', context)

def canteen(request, name):
    canteen = get_object_or_404(Canteen, name=name)
    cuisine_filter = request.GET.get('cuisine')  # Get cuisine filter from query parameters if available

    stalls = Stall.objects.filter(canteen=canteen)  # Get all stalls for the canteen
    
    if cuisine_filter:  # If a cuisine filter is applied
        stalls = stalls.filter(cuisine=cuisine_filter)  # Filter stalls by cuisine

    # Calculate price range for each stall
    stalls_with_prices = []
    for stall in stalls:
        products = Product.objects.filter(stall=stall)
        if products.exists():
            min_price = products.order_by('price').first().price
            max_price = products.order_by('-price').first().price
            stalls_with_prices.append({
                'stall': stall,
                'min_price': min_price,
                'max_price': max_price
            })
        else:
            stalls_with_prices.append({
                'stall': stall,
                'min_price': None,
                'max_price': None
            })

    # Pass the list of available cuisines and filtered stalls to the template
    cuisines = Stall.objects.filter(canteen=canteen).values_list('cuisine', flat=True).distinct()  # Get distinct cuisines from filtered stalls
    context = {
        'faculty_name': canteen.faculty.name,
        'canteen_name': canteen.name,
        'stalls_with_prices': stalls_with_prices,
        'cuisines': cuisines,
        'current_cuisine': cuisine_filter,
    }
    return render(request, 'canteen.html', context)

def stall(request, canteen_name, stall_name):
    canteen = get_object_or_404(Canteen, name=canteen_name)
    
    # Filter stalls by canteen and name instead of using get_object_or_404
    stalls = Stall.objects.filter(canteen=canteen, name=stall_name)
    
    # If there are multiple stalls, select the first one or handle the situation as needed
    if stalls.exists():
        stall = stalls.first()  # Take the first stall that matches
        products = Product.objects.filter(stall=stall)
        
        context = {
            'products': products,
            'canteen_name': canteen_name,
            'stall_name': stall_name,  # <-- Added the missing comma here
            'stall': stall,
        }
        return render(request, 'stall.html', context)
    else:
        # Handle case where no stalls are found if needed
        messages.error(request, "No stalls found with that name.")
        return redirect('main:canteen', name=canteen_name)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'product.html', context)


@login_required(login_url='/login_and_register/')
def user_homepage(request):
    return

@user_passes_test(is_admin, login_url='/login_and_register/')
@login_required
def add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.is_ajax():  
                return JsonResponse({"success": True, "message": "Faculty added successfully!"})
            messages.success(request, 'Faculty added successfully!')
            return redirect('main:faculty')
        else:
            if request.is_ajax():  
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        form = FacultyForm()
    
    return render(request, 'add_faculty.html', {'form': form})

@user_passes_test(is_admin, login_url='/login_and_register/')
@login_required
def add_canteen(request):
    if request.method == 'POST':
        form = CanteenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.is_ajax():  
                return JsonResponse({"success": True, "message": "Canteen added successfully!"})
            messages.success(request, 'Canteen added successfully!')
            return redirect('main:faculty')
        else:
            if request.is_ajax(): 
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        form = CanteenForm()
    
    return render(request, 'add_canteen.html', {'form': form})

@user_passes_test(is_admin, login_url='/login_and_register/')
def add_stall(request):
    referer = request.META.get('HTTP_REFERER', reverse('main:homepage'))
    if request.method == 'POST':
        form = StallForm(request.POST)
        if form.is_valid():
            stall = form.save()
            canteen_name = stall.canteen.name
            return redirect('main:canteen', name=canteen_name)
    else:
        form = StallForm()
    return render(request, 'add_stall.html', {'form': form, 'referer': referer})

@user_passes_test(is_admin, login_url='/login_and_register/')
def delete_stall(request, stall_id):
    if request.method == 'POST':
        stall = get_object_or_404(Stall, id=stall_id)
        canteen_name = stall.canteen.name
        stall.delete()
        return redirect(reverse('main:canteen', kwargs={'name': canteen_name})) 
    
@user_passes_test(is_admin, login_url='/login_and_register/')
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        stall_name = product.stall.name
        canteen_name = product.stall.canteen.name
        product.delete()
        return redirect(reverse('main:stall', kwargs={'canteen_name': canteen_name, 'stall_name': stall_name}))

@user_passes_test(is_admin, login_url='/login_and_register/')
@login_required
def add_product(request, stall_id=None):
    stall = get_object_or_404(Stall, id=stall_id)  # Fetch the stall instance

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.stall = stall  # Associate product with the stall
            product.save()
            messages.success(request, 'Product added successfully!')

            # Redirect to the stall page using canteen_name and stall_name
            return redirect('main:stall', canteen_name=stall.canteen.name, stall_name=stall.name)
    else:
        form = ProductForm(initial={'stall': stall_id})

    context = {
        'form': form,
        'stall_id': stall_id,
    }
    return render(request, 'add_product.html', context)


@user_passes_test(is_admin, login_url='/login_and_register/')
def delete_faculty(request, faculty_id):
    if request.method == 'POST':
        faculty = get_object_or_404(Faculty, id=faculty_id)  # Match against 'id' field
        faculty.delete()
        return redirect('main:faculty')  # Redirect to the faculty listing page

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(product=product)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteProduct.objects.filter(user=request.user, product=product).exists()
    context = {
        'product': product,
        'reviews': reviews,
        'is_favorited': is_favorited,
    }
    return render(request, 'product.html', context)

@require_POST
@login_required(login_url='/login_and_register/')
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    rating = int(request.POST.get('rating'))
    comment = request.POST.get('comment', '')

    try:
        review, created = ProductReview.objects.get_or_create(
            product=product, user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        if not created:
            review.rating = rating
            review.comment = comment
            review.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'review': {
                    'id': review.id,
                    'rating': review.rating,
                    'comment': review.comment,
                    'user': review.user.username,
                    'created_at': review.created_at.strftime('%B %d, %Y')
                }
            })
        messages.success(request, 'Your review has been submitted successfully.')
        return redirect('main:product_detail', product_id=product.id)
    except IntegrityError:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'You have already reviewed this product.'})
        messages.error(request, 'You have already reviewed this product.')
        return redirect('main:product_detail', product_id=product.id)

@user_passes_test(is_admin, login_url='/login_and_register/')
def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    product = review.product  # Assuming ProductReview has a ForeignKey to Product
    review.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'review_id': review_id})
    messages.success(request, 'Review deleted successfully.')
    return redirect('main:product_detail', product_id=product.id)

@csrf_exempt
@login_required(login_url='/login_and_register/')
def favorite_product(request, product_id):
    # Validate product ID
    if product_id <= 0:
        return JsonResponse({'status': 'error', 'message': 'Invalid product ID'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    favorite, created = FavoriteProduct.objects.get_or_create(
        user=request.user, 
        product=product
    )
    return JsonResponse({
        'status': 'success',
        'message': 'Added to favorites' if created else 'Already in favorites'
    })

@csrf_exempt
@login_required(login_url='/login_and_register/')
def unfavorite_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = get_object_or_404(FavoriteProduct, user=request.user, product=product)
    favorite.delete()
    messages.success(request, 'Product removed from favorites.')
    return redirect('main:product_detail', product_id=product.id)

@login_required(login_url='/login_and_register/')
def favorite_products(request):
    favorites = FavoriteProduct.objects.filter(user=request.user).select_related('product')
    context = {
        'favorites': favorites
    }
    return render(request, 'favorite_products.html', context)

@csrf_exempt
def show_json(request):
    users = User.objects.all()
    faculties = Faculty.objects.all()
    canteens = Canteen.objects.all()
    stalls = Stall.objects.all()
    products = Product.objects.all()
    reviews = ProductReview.objects.all()
    favorite_products = FavoriteProduct.objects.all()

    data = {
        'users': json.loads(serializers.serialize('json', users)),
        'faculties': json.loads(serializers.serialize('json', faculties)),
        'canteens': json.loads(serializers.serialize('json', canteens)),
        'stalls': json.loads(serializers.serialize('json', stalls)),
        'products': json.loads(serializers.serialize('json', products)),
        'reviews': json.loads(serializers.serialize('json', reviews)),
        'favorite_products': json.loads(serializers.serialize('json', favorite_products)),
    }

    pretty_data = json.dumps(data, indent=4)

    return HttpResponse(pretty_data, content_type='application/json')


@user_passes_test(is_admin, login_url='/login_and_register/')
@login_required
def edit_faculty(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faculty updated successfully!')
            return redirect('main:faculty')
        else:
            if request.is_ajax():  
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        form = FacultyForm(instance=faculty)
    
    return render(request, 'edit_faculty.html', {'form': form, 'faculty': faculty})

@csrf_exempt
def get_stall_json(request, stall_id):
    stall = get_object_or_404(Stall, id=stall_id)
    return JsonResponse({
        "name": stall.name,
        "canteen": stall.canteen.name,
        "cuisine": stall.cuisine,
        "products": list(stall.products.values())
    })

@csrf_exempt
def create_stall_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = StallForm(data)
        if form.is_valid():
            stall = form.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})

@csrf_exempt
def update_stall_flutter(request, stall_id):
    if request.method == 'PUT':
        stall = get_object_or_404(Stall, id=stall_id)
        data = json.loads(request.body)
        form = StallForm(data, instance=stall)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@csrf_exempt
def delete_stall_flutter(request, stall_id):
    if request.method == 'DELETE':
        stall = get_object_or_404(Stall, id=stall_id)
        stall.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@csrf_exempt
@login_required(login_url='/login_and_register/')
def get_favorites_json(request):
    favorites = FavoriteProduct.objects.filter(user=request.user).select_related('product__stall')
    return JsonResponse([
        {
            'id': favorite.id,
            'product': {
                'id': favorite.product.id,
                'name': favorite.product.name,
                'price': str(favorite.product.price),
                # Return stall info as nested object
                'stall': {
                    'id': favorite.product.stall.id,
                    'name': favorite.product.stall.name,
                }
            }
        }
        for favorite in favorites
    ], safe=False)

@csrf_exempt
def submit_review_flutter(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed.'}, status=405)

    try:
        # Parse JSON body
        data = json.loads(request.body)
        product_id = data.get('product_id')
        rating = data.get('rating')
        comment = data.get('comment')

        # Validate input
        if not product_id or not rating:
            return JsonResponse({'success': False, 'error': 'Product ID and rating are required.'}, status=400)

        product = get_object_or_404(Product, id=product_id)

        # Create or update review
        review, created = ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )

        return JsonResponse({
            'success': True,
            'review': {
                'id': review.id,
                'product_id': product.id,
                'rating': review.rating,
                'comment': review.comment,
                'user': review.user.username,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            },
        })

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def delete_review_flutter(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed.'}, status=405)

    try:
        # Parse JSON body
        data = json.loads(request.body)
        review_id = data.get('review_id')

        # Validate input
        if not review_id:
            return JsonResponse({'success': False, 'error': 'Review ID is required.'}, status=400)

        # Fetch and delete the review
        review = get_object_or_404(ProductReview, id=review_id, user=request.user)
        review.delete()

        return JsonResponse({'success': True, 'message': 'Review deleted successfully.'})

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    

@csrf_exempt
def create_faculty_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            new_faculty = Faculty.objects.create(
                name=data["name"],
                nickname=data["nickname"],
                colors=data["colors"],
                image=data["image"]
            )
            new_faculty.save()
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Faculty, Canteen

@csrf_exempt
def create_canteen_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Add logging to see the received data
            faculty = Faculty.objects.get(name=data["faculty"])
            new_canteen = Canteen.objects.create(
                name=data["name"],
                faculty=faculty,
                image=data["image"],
                price=data["price"]
            )
            new_canteen.save()
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            print("Error:", str(e))  # Add logging to see the error
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def get_product_json(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        "model": "main.product",
        "pk": product.id,
        "fields": {
            "name": product.name,
            "price": str(product.price),
            "stall": {
                "id": product.stall.id,
                "name": product.stall.name,
                "canteen": product.stall.canteen.name,
            }
        }
    }
    return JsonResponse(data)

#filtering products by stall
@csrf_exempt
def products_json(request):
    """
    Returns a JSON response containing products.
    If a 'stall_id' query parameter is provided, filters products by the given stall.
    """
    stall_id = request.GET.get('stall_id', None)
    
    if stall_id:
        try:
            stall_id = int(stall_id)
            products = Product.objects.filter(stall_id=stall_id)
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid stall_id parameter."}, status=400)
    else:
        products = Product.objects.all()
    
    # Serialize the products
    serialized_products = serializers.serialize('json', products)
    products_json = json.loads(serialized_products)
    
    # Return as JSON
    return JsonResponse({"products": products_json}, safe=False)