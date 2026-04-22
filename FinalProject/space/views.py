from django.shortcuts import render
from . import api
import pprint

# Create your views here.
def index(request):
    return render(request, 'space/index.html')

#get all the images from the api
def view_all(request):
    data = api.get_all()

    return render(request, 'space/view_images.html', {'data':data})

#get all the images from last week
def last_week(request):
    data = api.last_week()
    pprint.pprint(data)
    return render(request, 'space/view_images.html', {'data':data})
