# urls.py

from django.urls import path
from main.views import (
    homepage, logout_user, faculty, canteen, stall, product_detail, 
    user_homepage, add_canteen, add_stall, delete_stall, 
    add_product, delete_faculty, show_json, login_and_register, delete_product,
    submit_review, delete_review, favorite_product, unfavorite_product, favorite_products,
    add_faculty, edit_faculty, get_stall_json, create_stall_flutter, update_stall_flutter, delete_stall_flutter, get_favorites_json,
    submit_review_flutter, delete_review_flutter, create_faculty_flutter, create_canteen_flutter, get_product_json, create_product_flutter,
    delete_product_flutter, edit_product_flutter, products_json
)

app_name = 'main'

urlpatterns = [
    # Homepage and Authentication
    path('', homepage, name='homepage'),
    path('logout/', logout_user, name='logout'),
    path('login_and_register/', login_and_register, name='login_and_register'),
    
    # Faculty, Canteen, Stall, Product navigation
    path('faculty/', faculty, name='faculty'),                          # Faculty listing page
    path('canteen/<str:name>/', canteen, name='canteen'),               # Canteen listing by faculty name
    path('canteen/<str:canteen_name>/<str:stall_name>/', stall, name='stall'),  # Stall listing by canteen and stall names
    path('product/<int:product_id>/', product_detail, name='product_detail'),   # Product detail by product ID
    path('add_product/<int:stall_id>/', add_product, name='add_product'),
    path('get-product/<int:product_id>/', get_product_json, name='get_product_json'),
    path('products_json/', products_json, name='products_json'),

    # Review submission
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),  
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),  

    # Favorite products
    path('favorites/', favorite_products, name='favorite_products'),
    path('favorites/<int:product_id>/', favorite_product, name='favorite_product'),
    path('unfavorite/<int:product_id>/', unfavorite_product, name='unfavorite_product'),  
    path('favorites/json/', get_favorites_json, name='get_favorites_json'),
    path('favorite/<int:product_id>/', favorite_product, name='favorite_product'),

    # CRUD operations (admin restricted)
    path('add-faculty/', add_faculty, name='add_faculty'),  # Add this line
    path('add-canteen/', add_canteen, name='add_canteen'),  # Add this line
    path('user_homepage/', user_homepage, name='user_homepage'),          # Admin/User homepage
    path('edit_faculty/<int:faculty_id>/', edit_faculty, name='edit_faculty'), # Admin: edit faculty
    # path('add_canteen/', add_canteen, name='add_canteen'),                # Admin: add canteen
    path('add_stall/', add_stall, name='add_stall'),                      # Admin: add stall
    path('stall/delete/<int:stall_id>/', delete_stall, name='delete_stall'),  # Admin: delete stall
    path('add_product/', add_product, name='add_product'),                # Admin: add product
    path('add_product/<int:stall_id>/', add_product, name='add_product'), # Admin: add product to specific stall
    path('faculty/delete/<int:faculty_id>/', delete_faculty, name='delete_faculty'), # Admin: delete faculty
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    
    # Flutter
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),
    path('delete-product-flutter/<int:product_id>/', delete_product_flutter, name='delete_product_flutter'),
    path('edit-product-flutter/<int:id>/', edit_product_flutter, name='edit_product_flutter'),
    
    # JSON data endpoint for external use
    path('show_json/', show_json, name='show_json'),

    #### Flutter urls ####

    # JSON data endpoint for Flutter
    path('get-stall/<int:stall_id>/', get_stall_json, name='get_stall_json'),

    # CRUD operations for Flutter
    path('create-stall-flutter/', create_stall_flutter, name='create_stall_flutter'),
    path('update-stall-flutter/<int:stall_id>/', update_stall_flutter, name='update_stall_flutter'),
    path('delete-stall-flutter/<int:stall_id>/', delete_stall_flutter, name='delete_stall_flutter'),
    path('submit-review-flutter/', submit_review_flutter, name='submit_review_flutter'),
    path('delete-review-flutter/', delete_review_flutter, name='delete_review_flutter'),
    path('create-faculty-flutter/', create_faculty_flutter, name='create_faculty_flutter'),
    path('create-canteen-flutter/', create_canteen_flutter, name='create_canteen_flutter'),
]
