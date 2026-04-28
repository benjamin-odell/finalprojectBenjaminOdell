# INF601 - Advanced Programming in Python
# Benjamin Odell
# Final Project
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Image(models.Model):
    date = models.DateField()
    likes = models.IntegerField(default=0)
    data = models.JSONField(default=dict)
    amt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date) + " " + str(self.data['title'] if 'title' in self.data else self.data)

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.user.username + " likes " + str(self.date.date())

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " comments on " + str(self.image.data['title'] if 'title' in self.image.data else self.image.data)




