#this file is for interaction with the NASA APOD API
import requests
from dotenv import load_dotenv
import os
import requests
from datetime import timedelta, datetime

load_dotenv()


API_KEY = os.getenv("API_KEY")

url = 'https://api.nasa.gov/planetary/apod'

payload = {'api_key': API_KEY, 'start_date': None, 'end_date': None}


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

    return data.json()
