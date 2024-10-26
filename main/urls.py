from django.urls import path
# from main.views import show_main
from main.views import homepage, register, login_user, logout_user \
    , faculty, canteen, add_faculty, user_homepage, add_canteen, add_stall, \
    add_product, delete_faculty, show_json, stall

app_name = 'main'

urlpatterns = [
    # path('', show_main, name='show_main'),
    path('', homepage, name='homepage'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('faculty/', faculty, name='faculty'),
    path('canteen/<str:name>/', canteen, name='canteen'),
    path('add_faculty/', add_faculty, name='add_faculty'),
    path('user_homepage/', user_homepage, name='user_homepage'),  # User homepage
    path('add_canteen/', add_canteen, name='add_canteen'),  # Admin canteen addition
    path('add_stall/', add_stall, name='add_stall'),        # Admin stall addition
    path('add_product/', add_product, name='add_product'),  # Admin product addition
    path('faculty/delete/<int:faculty_id>/', delete_faculty, name='delete_faculty'),
    path('show_json/', show_json, name='show_json'),
    path('canteen/<str:canteen_name>/stalls/', stall, name='stall'),
]