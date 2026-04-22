from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('view_all', views.view_all, name='view_all'),
    path('last_week', views.last_week, name='last_week'),
]