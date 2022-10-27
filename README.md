# USER_APP
This is a simple Django application powered also by Geodjango, The Application contains full user authentication
and display registered users on a leaflet map as point data


# A demo application about the project is hosted on heroku
## click the link to view the demo

## https://users-webapp.herokuapp.com/

## Dependencies:
- Geodjango Dependencies (Geos,
- GDAL, and PROJ4)
- Spatial Database.
- psycopg2-binary
- Python.
- Django(Geodjango).
- Python Leaflet package.


## Demo Application Preview
![Screenshot (419)](https://user-images.githubusercontent.com/43718849/198394828-e8557861-86b6-4575-a9a7-b38507b609f1.png)


Main features
    Separated dev and production settings

    Account app with Custom User Model

    Bootstrap static files included

    User registration and logging process

    Map Interface to show All Registered users on a leaflet Map

    Procfile for easy deployments on Heroku

    

# Local development
## To run this project in your development machine, follow these steps:
## clone the repository by running the following in command Prompt:

    git clone https://github.com/Kevin-Sambuli/user-app.git
    cd user-app


## Create a virtual environment to install dependencies in and activate it

    python -m venv venv


## On Windows Activate the virtual environment:
    venv\Scripts\activate


## Then install the dependencies:

    pip install -r requirements.txt


## If you have PostgreSQL installed you can Create a development database by doing the following:
### NOTE: Change the Environment variables in the example env file to meet your database credentials:

1. Create a Postgis enabled database to support spatial objects

## To Create the tables in the database run

    python manage.py migrate

## If everything is alright, you should be able to start the Django development server:

    python manage.py runserver 

Open your browser and go to http://127.0.0.1:8000, you will be greeted with a welcome page.

## Create a Super User so that you can add several users to the database:
    python manage.py createsuperuser

## To Run the Tests
### In order to run test the for the mode, views, form and urls just use the following command
### The application uses the default django unittest module to run the applications tests:
    python manage.py test

## Authentication Process
- In order to test the the application flows fill in the account registration  by clicking the register button on the Navigation bar.


# Walkthrough.
## Registration
1. After Successful registration an email will be sent to your registration email that will prompt you to activate your account
2. Click the link in your email account to activate your account
3. You'll be redirected to the home page as an authenticated user

## Authorized users with object level permission can view their own account on nthe admin page

![Screenshot (413)](https://user-images.githubusercontent.com/43718849/198390330-ef45be94-34f8-4da3-bac3-4739c56cf442.png)


## A user without object level permission to a certain object is denied the permission to vier the object as shown below
![Screenshot (412)](https://user-images.githubusercontent.com/43718849/198390629-3c7dd4c0-4daf-4a7c-b9ec-7bc54d3a6d3c.png)



## upcoming development
- Dockerizingg the application witth Docker
- serving the front end with React
- Serving the app with Geoserver layer
