#this file is for interaction with the NASA APOD API
import requests
from dotenv import load_dotenv
import os
import requests
from datetime import timedelta, datetime
from .models import Image
import pprint
import json

load_dotenv()


API_KEY = os.getenv("API_KEY")

url = 'https://api.nasa.gov/planetary/apod'

payload = {'api_key': API_KEY, 'start_date': None, 'end_date': None, 'date': None}


def get_all():
    payload['start_date'] = '1995-06-16'
    data = requests.get(url, params=payload)
    print(data.text)

    return data

def last_week():
    date = datetime.today() - timedelta(days=7)
    date = date.date()
    payload['start_date'] = date

    data = requests.get(url, params=payload)
    print(data.text)

    return data.json()

def last_x(x):
    data = []
    for t in range(x):
        date = datetime.today() - timedelta(days=t)
        print(date)
        d = get_date(date)
        print(type(d))
        data.append(d)

    return data

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
        response = requests.get(url, params=payload)
        if response.status_code == 200: #the request went through
            img.data = response.json()
            img.date = date.date()
            img.save()
        else:
            raise
    else: #the image is in the database so we can just return that info
        if(img.data == {}): #try to update image with the most up to date info
            payload['date'] = date.date()
            response = requests.get(url, params=payload)
            if(response.status_code == 200): #request when through
                img.data = response.json()
                img.amt = 0
                img.save()
        img.amt = img.amt + 1
        img.save()
    #returns the image data
    return img.data
