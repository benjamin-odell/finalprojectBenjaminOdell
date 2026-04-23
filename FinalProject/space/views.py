from django.shortcuts import render
from . import api
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

#get all the images from last week
def last_week(request):
    try:
        data = api.last_x(7)
        return render(request, 'space/view_images.html', {'data': data})
    except:
        return render(request, 'space/api_error.html')

def random_view(request):
    data = api.get_random(10)
    pprint.pprint(data)
    return render(request, 'space/view_images.html', {'data': data})


def detail(request, date):
    try:
        img = api.get_date(date)
        return render(request, 'space/details.html', {'img': img})
    except:
        return render(request, 'space/api_error.html')



