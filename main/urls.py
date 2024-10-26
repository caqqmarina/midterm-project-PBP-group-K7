from django.urls import path
# from main.views import show_main
from main.views import homepage, register, login_user, logout_user \
    , faculty, canteen, add_faculty_and_canteen, user_homepage, add_canteen, add_stall, \
    add_product, delete_faculty, show_json, stall, product_detail

app_name = 'main'

urlpatterns = [
    # path('', show_main, name='show_main'),
    path('', homepage, name='homepage'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('faculty/', faculty, name='faculty'),
    path('canteen/<str:name>/', canteen, name='canteen'),
    path('add-faculty-canteen/', add_faculty_and_canteen, name='add_faculty_and_canteen'),
    path('user_homepage/', user_homepage, name='user_homepage'),  # User homepage
    path('add_canteen/', add_canteen, name='add_canteen'),  # Admin canteen addition
    path('add_stall/', add_stall, name='add_stall'),        # Admin stall addition
    path('add_product/', add_product, name='add_product'),  # Admin product addition
    path('faculty/delete/<int:faculty_id>/', delete_faculty, name='delete_faculty'),
    path('show_json/', show_json, name='show_json'),
    path('canteen/<str:canteen_name>/<str:stall_name>/', stall, name='stall'),
    path('add_product/<int:stall_id>/', add_product, name='add_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]