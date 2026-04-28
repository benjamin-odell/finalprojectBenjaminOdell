# INF601 - Advanced Programming in Python
# Benjamin Odell
# Final Project
#this file is for interaction with the NASA APOD API
import requests
from dotenv import load_dotenv
import os
import requests
from datetime import timedelta, datetime
from .models import Image
import pprint
import pytz
import json
from random import randrange

load_dotenv()


API_KEY = os.getenv("API_KEY")

url = 'https://api.nasa.gov/planetary/apod'

payload = {'api_key': API_KEY}

random_likes = True


def last_x(x):
    data = []
    t = 0
    while t < x:
        date = datetime.now() - timedelta(days=t)
        print(date.date())
        d = get_date(date)
        print(d)
        #check for 404
        if d:
            data.append(d)
        else:
            x = x+1

        t = t + 1

    return data

#get a random amount of images from the APOD api
def get_random(x):
    max = datetime(1995, 6,16)
    delta = datetime.today() - max
    delta = delta.days
    data = []
    days = []
    dates = []

    for _ in range(x):#loops through the amt specified
        while True: #loops until we find a random day not in the set
            r = randrange(0, delta) #gets random day
            if r not in days: #check
                days.append(r)
                break

    for d in days:
        date = datetime.today() - timedelta(days=d)
        dates.append(str(date.date()))
        date = get_date(date)
        data.append(date)
        pprint.pprint(data)

    return data, dates

#gets the image for a date. It first check to see if we have the image in the database, if not fetches it from the API
def get_date(date):
    #first check the database
    try:
        img = Image.objects.get(date=date)
    except Image.DoesNotExist:
        img = None
    if img is None:  #add image to the database
        #fetch image data for the date
        img = Image.objects.create(date=date)
        payload['date'] = date.date()
        while True:
            response = requests.get(url, params=payload)
            print(response.status_code)
            print(response.headers)
            if response.status_code == 200: #the request went through
                img.data = response.json()
                img.date = date.date()
                if random_likes:
                    img.likes = randrange(0, 1000)
                img.save()
                break
            if response.status_code == 404:
                return None
    else: #the image is in the database so we can just return that info
        if(img.data == {}): #try to update image with the most up to date info
            payload['date'] = date.date()
            while True:
                response = requests.get(url, params=payload)
                print(response.status_code)
                print(response.headers)
                if(response.status_code == 200): #request when through
                    img.data = response.json()
                    img.amt = 0
                    img.save()
                    break
                if response.status_code == 404:
                    return None
    #returns the image data
    return img

def get_dates(dates):
    ans = []
    for date in dates:
        ans.append(get_date(date))

    return ans