from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from . import api
from .models import Likes, Image
import pprint

# Create your views here.
def index(request):
    return render(request, 'space/index.html')

#get all the images from the api
def view_all(request):
    try:
        data = api.get_all()
        return render(request, 'space/view_images.html', {'data':data})
    except:
        return render(request, 'space/api_error.html')

def get_liked(request):
    if request.user.is_authenticated:
        liked = Likes.objects.filter(user=request.user)
        liked_id = []
        for l in liked:
            date = api.get_date(l.date)
            liked_id.append(date.id)
        return liked_id
    else:
        return []

#get all the images from last week
def last_week(request):
    data = api.last_x(7)
    #check if user is loged in
    liked = get_liked(request)
    print(liked)
    return render(request, 'space/view_images.html', {'data': data, 'liked': liked})

def random_view(request):
    data = api.get_random(10)
    liked = get_liked(request)
    return render(request, 'space/view_images.html', {'data': data, 'liked': liked})

#prints out all the details of an image
def detail(request, date):
    try:
        img = api.get_date(date)
        liked = get_liked(request)
        return render(request, 'space/details.html', {'img': img, 'liked': liked})
    except:
        return render(request, 'space/api_error.html')

@login_required
def like(request, date):
    #first check if user has already liked the img
    check = Likes.objects.filter(user=request.user, date=date)
    print(check)

    if not check.exists():
        #incress number of likes
        img, created = Image.objects.get_or_create(date=date)
        img.likes = img.likes + 1
        img.save()

        #creat like entry in the database
        like = Likes(user=request.user, date=date)
        like.save()

    next_url = request.POST.get('next', '/')
    return HttpResponseRedirect(next_url)

@login_required
def unlike(request, date):
    #get like
    like = Likes.objects.filter(user=request.user, date=date)

    if like.exists():
        #lower dates like amount
        img = Image.objects.get(date=date)
        img.likes = img.likes - 1
        img.save()

        #delete like
        like.delete()

    next_url = request.POST.get('next', '/')
    return HttpResponseRedirect(next_url)


@login_required
def liked_view(request):
    #get the dates for all liked views
    liked = Likes.objects.filter(user=request.user)

    dates = []
    for like in liked:
        dates.append(like.date)

    data = api.get_dates(dates)
    liked = get_liked(request)

    return render(request, 'space/view_images.html', {'data': data, 'liked': liked})





