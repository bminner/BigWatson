from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('result/', views.result, name='result'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tryit/', views.tryit, name='tryit'),
    path('tryit_results/', views.tryit_results, name='tryit_results'),
]
