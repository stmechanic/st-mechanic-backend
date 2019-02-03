# St.Mechanic

## What is it?
The API that powers the St.Mechanic frontend


## Installation

### Instal prerequisites:
* Get Python 3.6 [here](https://www.python.org/downloads/)  
* Get pipenv [here](https://github.com/pypa/pipenv)  
* Get postgres [here](http://postgresguide.com/setup/install.html)  


Clone the repo
```
$ git clone https://github.com/alexkiura/st-mechanic-backend.git
```

Navigate to the root folder
```
$ cd st-mechanic-backend
```
Create a python 3.6 environment
```
$ pipenv --python 3.6
```
Install the necessary packages
```
$ pipenv install --dev
```

### Setup the database:
Create the database:
Ensure postgres is running.
```
$ psql
$ CREATE DATABASE st-mechanic;
```



Perform migrations by running:
* `python manage.py makemigrations`
* `python manage.py migrate`

Start the development server by running `python manage.py runserver`


## Testing
To run the tests for the app:
```
pipenv run coverage run manage.py test
```
pipenv run coverage run manage.py test

To get coverage:
```
coverage report -m
```

## Technologies used
[Django](https://www.djangoproject.com/) |
[Django REST](http://www.django-rest-framework.org/)
