from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Image(models.Model):
    date = models.DateField()
    likes = models.IntegerField(default=0)

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.DateTimeField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.DateTimeField()
    comment = models.TextField()




