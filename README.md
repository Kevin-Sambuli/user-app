# user-app
the app is used for user registration and display them on a map using leaflet
# USER_APP
This is a simple Django application powered also by Geodjango, The Application contains full user authentication
and display registered users on a leaflet map as point data

![Screenshot (414)](https://user-images.githubusercontent.com/43718849/198390042-ad6e6811-22a2-42de-82c2-b51f25194705.png)


Main features
    Separated dev and production settings

    Account app with Custom User Model

    Bootstrap static files included

    User registration and logging process

    Map Interface to show All Registered users on a leaflet Map

    Procfile for easy deployments on Heroku

    


Dependencies:
    - Geodjango Dependencies (Geos, GDAL, and PROJ4)
    - Spatial Database-PostgreSQL/PostGIS.
    - psycopg2-binary
    - Python.
    - Django(Geodjango).
    - Javascript Leaflet Library.

# Local development
To run this project in your development machine, follow these steps:
clone the repository by running the following in command Prompt:

```
git clone https://github.com/Kevin-Sambuli/user-app.git
cd user-app
```

## Create a virtual environment to install dependencies in and activate it
```
python -m venv venv
```

## Activate the virtual environment:
```
venv\Scripts\activate
```

## Then install the dependencies:
```

pip install -r requirements.txt
```

## If you have PostgreSQL installed you can Create a development database by doing the following:

1. Create a Postgis enabled database to support spatial objects
2. To Create the tables in the database run

## NOTE: Change the Environment variables in the example env file to meet your database credentials:
    ```
    python manage.py migrate ```

## If everything is alright, you should be able to start the Django development server:
    ``` python manage.py runserver ```

Open your browser and go to http://127.0.0.1:8000, you will be greeted with a welcome page.

## Create a Super User so that you can add several users to the database:
``` python manage.py createsuperuser ```

## To Run tThe Tests
- In order to run test the for the mode, views, form and urls just use the following command
The application uses the default django unittest module to run the applications tests
``` python manage.py test```

## Authentication Process
- In order to test the the application flows fill in the account registration  by clicking the register button on the Navigation bar.



# Walkthrough.
## Registration
1. After Successful registration an email will be sent to your registration email that will prompt you to activate your account
2. Click the link to activate your account
3. Your account will be activated and You'll be redirected to the home page as an authenticated user

## Authorized users with object level permission can view their own account account

![Screenshot (413)](https://user-images.githubusercontent.com/43718849/198390330-ef45be94-34f8-4da3-bac3-4739c56cf442.png)


## A user without object level permission to a certain object is denied the permission to vier the object as shown below
![Screenshot (412)](https://user-images.githubusercontent.com/43718849/198390629-3c7dd4c0-4daf-4a7c-b9ec-7bc54d3a6d3c.png)



## Production
### If you are NOT using Makefile
```
cd user-app
run the command: docker-compose --build -d --remove-orphans
navigate to localhost:8000
```

