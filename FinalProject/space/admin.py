from django.contrib import admin

from .models import Image, Comment, Likes

# Register your models here.
admin.site.register(Image)
admin.site.register(Likes)
admin.site.register(Comment)