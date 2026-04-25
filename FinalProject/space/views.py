import urllib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from . import api
from .models import Likes, Image, Comment
from urllib.parse import urlencode
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

#gets all of a users likes
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

#get the comments of an image
def get_comments(img):
    comments = Comment.objects.filter(image=img).order_by('-timestamp')
    return comments

#get all the images from last week
def last_week(request):
    data = api.last_x(7)
    #check if user is loged in
    liked = get_liked(request)
    print(liked)
    request.session['refresh'] = False
    return render(request, 'space/view_images.html', {'data': data, 'liked': liked})

def random_view(request):
    refresh = request.session.get('refresh', False)
    if not refresh:
        data, dates = api.get_random(3)
        request.session['dates'] = dates
    else:
        dates = request.session['dates']
        data = api.get_dates(dates)
    liked = get_liked(request)
    request.session['refresh'] = False
    return render(request, 'space/view_images.html', {'data': data, 'liked': liked})

#prints out all the details of an image
def detail(request, date):
    img = api.get_date(date)
    liked = get_liked(request)
    comments = get_comments(img)
    request.session['refresh'] = False
    return render(request, 'space/details.html', {'img': img,
                                                  'liked': liked,
                                                  'comments': comments})

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
    request.session['refresh'] = True
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
    request.session['refresh'] = True
    return HttpResponseRedirect(next_url)


@login_required
def liked_view(request):
    #get the dates for all liked views
    liked = Likes.objects.filter(user=request.user)

    dates = []
    for l in liked:
        dates.append(l.date)


    data = api.get_dates(dates)
    liked = get_liked(request)
    request.session['refresh'] = False
    return render(request, 'space/view_images.html', {'data': data, 'liked': liked})

#Add comment view
@login_required
def add_comment(request, date):
    #check for post
    error = None
    liked = get_liked(request)
    img = api.get_date(date)
    request.session['refresh'] = False
    if request.method == 'POST':
        #check for comment text
        comment_text = request.POST.get('comment')
        if comment_text is None or comment_text == '':
            error = 'Comment text is required'
        else:
            #create comment
            comment = Comment(user=request.user, image=img, comment=comment_text)
            #save comment
            comment.save()
            #redirect to details page
            return redirect(reverse('details', kwargs={'date': date}))

    #return comment page
    comments = get_comments(img)
    return render(request, 'space/comment.html', {'img': img,
                                                  'liked': liked,
                                                  'error': error,
                                                  'comments': comments})

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    date = comment.image.date
    #verify that the logged-in user owns the comment
    if request.user.id == comment.user.id:
        comment.delete()

    return HttpResponseRedirect(reverse('details', kwargs={'date': date}))







