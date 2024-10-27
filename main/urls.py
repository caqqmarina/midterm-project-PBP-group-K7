# urls.py

from django.urls import path
from main.views import (
    homepage, logout_user, faculty, canteen, stall, product_detail, 
    add_faculty_and_canteen, user_homepage, add_canteen, add_stall, delete_stall, 
    add_product, delete_faculty, show_json, login_and_register, delete_product
)

app_name = 'main'

urlpatterns = [
    # Homepage and Authentication
    path('', homepage, name='homepage'),
    path('logout/', logout_user, name='logout'),
    path('login_and_register/', login_and_register, name='login_and_register'),
    
    # Faculty, Canteen, Stall, Product navigation
    path('faculty/', faculty, name='faculty'),                          # Faculty listing page
    path('canteen/<str:faculty_name>/', canteen, name='canteen'),               # Canteen listing by faculty name
    path('canteen/<str:canteen_name>/<str:stall_name>/', stall, name='stall'),  # Stall listing by canteen and stall names
    path('product/<int:product_id>/', product_detail, name='product_detail'),   # Product detail by product ID
    path('add_product/<int:stall_id>/', add_product, name='add_product'),

    # CRUD operations (admin restricted)
    path('add-faculty-canteen/', add_faculty_and_canteen, name='add_faculty_and_canteen'),
    path('user_homepage/', user_homepage, name='user_homepage'),          # Admin/User homepage
    # path('add_canteen/', add_canteen, name='add_canteen'),                # Admin: add canteen
    path('add_stall/', add_stall, name='add_stall'),                      # Admin: add stall
    path('stall/delete/<int:stall_id>/', delete_stall, name='delete_stall'),  # Admin: delete stall
    path('add_product/', add_product, name='add_product'),                # Admin: add product
    path('add_product/<int:stall_id>/', add_product, name='add_product'), # Admin: add product to specific stall
    path('faculty/delete/<int:faculty_id>/', delete_faculty, name='delete_faculty'), # Admin: delete faculty
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    
    # JSON data endpoint for external use
    path('show_json/', show_json, name='show_json'),
]
