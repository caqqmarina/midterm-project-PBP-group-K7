from django.urls import path
# from main.views import show_main
from main.views import homepage

app_name = 'main'

urlpatterns = [
    # path('', show_main, name='show_main'),
    path('', homepage, name='homepage'),
]