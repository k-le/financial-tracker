from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='budgeter-home'),
    path('about/', views.about, name='budgeter-about'),
    path('contact/', views.contact, name='budgeter-contact')
]
