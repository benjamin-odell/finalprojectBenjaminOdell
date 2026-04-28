### INF601 - Advanced Programming in Python
### Benjamin Odell
### Mini Project 4

# Space App

This is a web app for viewing the NASA APOD api. You can like images and add comments. 

### API Key
First you will need to get an APOD api key from [here](https://api.nasa.gov/)<br>
You can use: <b>DEMO_KEY</b> as the api key but you will be severely rate limited
<br>
After getting your API key create a <b>.env</b> file the <b>finalprojectBenjaminOdell</b> folder
<br>
Copy this into that file

```angular2html
API_KEY="DEMO_KEY"
```
Replace DEMO_KEY with your api key.

### Dependencies

install the python dependencies with the command
```angular2html
pip install -r requirements.txt
```
 
### Installing
 
Make sure to CD into the FinalProject folder with the manage.py file<br>
Run the command
```angular2html
python manage.py makemigrations
```
* This makes  the SQL that we need for the database<br>
Then run the command to apply the migration
```angular2html
python manage.py migrate
```

* You can set up the admin account with the command
```angular2html
python manage.py createsuperuser
```
 
### Executing program

Now you can run the server by running the command
```
python manage.py runserver
```

You can then access the site at [localhost:8000](http://localhost:8000/)<br>
You can find the admin page at [localhost:8000/admin](http://localhost:8000/admin)

### Notes
* The API can be quite slow so the database will cache the data from the API for future use
* The first time an Image from the API is cached it will be granted a random number of likes to simulate uses on the 
platform this can be disabled by changing random_likes in api.py in the space app to False
 
## Authors

Benjamin Odell - benjamin.m.odell@proton.me

## Acknowledgments
 
Inspiration, code snippets, etc.
* [Date Addition](https://www.geeksforgeeks.org/python/how-to-add-and-subtract-days-using-datetime-in-python/)
* [APOD API](https://api.nasa.gov/)
* [APOD Docs](https://github.com/nasa/apod-api)
* [Redirect to Previous Page](https://stackoverflow.com/questions/35796195/how-to-redirect-to-previous-page-in-django-after-post-request)
* [Deep Seek Chat: Used for Bootstrap and home page](https://chat.deepseek.com/share/d8zkukjswc9gqyum28)