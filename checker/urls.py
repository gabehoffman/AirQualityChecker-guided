from django.urls import path
from . import views

urlpatterns = [
    path('', views.location_view, name='location_form'),
]
