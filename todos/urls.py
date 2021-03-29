from django.urls import path

from .views import index, search

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
]
