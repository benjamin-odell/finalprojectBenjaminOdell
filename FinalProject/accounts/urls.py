from django.urls import path

from . import views

urlpatterns = [
    path('login', views.create_account, name='index'),
]