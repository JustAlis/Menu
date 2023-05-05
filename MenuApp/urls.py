from .views import *
from django.urls import re_path

urlpatterns = [
     re_path(r'^(?P<path>([^/]+/)*)$', menu_view, name='menu_url'),
]