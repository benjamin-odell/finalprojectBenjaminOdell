from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
def create_account(request):
    error = None
    if request.method == "POST":
        #create user

        #check for username and password
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username is None:
            error = "Username is required."
        elif password is None:
            error = "Password is required."
        else:
            #check for user
            user = User.objects.filter(username=username)
            if user:
                error = "Username already exists."
            else:
                User.objects.create_user(username=username, password=password)
                return HttpResponseRedirect(reverse("login"))

    #render page
    return render(request, 'accounts/create_user.html', {"error": error})

def login(request):
    pass