from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('view_all', views.view_all, name='view_all'),
    path('last_week', views.last_week, name='last_week'),
    path('detail/<date>', views.detail, name='details'),
    path('random', views.random_view, name='random'),
    path('random/<refresh>', views.random_view, name='random_refresh'),
    path('like/<date>', views.like, name='like'),
    path('unlike/<date>', views.unlike, name='unlike'),
    path('view_liked', views.liked_view, name='liked_view'),
    path('comment/<date>', views.add_comment, name='comment'),
    path('comment/delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('popular', views.most_liked, name='popular'),
]