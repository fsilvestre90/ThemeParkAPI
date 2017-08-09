MagicRideAPI
----------

This project showcases my vision on how the Theme Park API server should be implemented.

The main goals that were achieved:

* User login
* Get a single park by id
* Retrieve the parks filtered by a point, polyline, and other criteria
* Create a review

### Notes

I have implemented a majority of the endpoints, some I just copied parts of the other endpoint to show what
it could look like. I also created some dummy data scripts, check the installation instructions below.

Each endpoint has a certain set of parameters it accepts. You can view each parameter in the model folder.

The search for parks endpoints all use POST requests. I understand a GET would be ideal to be properly RESTful,
however since we are sending over large items of data (i.e. filters, polylines,etc) I ran into parsing issues. The
easiest solution right now was to make it a post and easily accept the parameters. If I had extra time solve that.

I would also like to use the strategy pattern for the /nearest/ endpoint based on the search param. It looks
nicer than if statements and is modular if we need to do changes.

Parks usually build and add rides so I thought it would make sense to create a ride within the park endpoint.
Same idea with Bookmarks and reviews.

Installation
------------

## Docker
Easiest way to run this server is using Docker:

    $ docker-compose up --build

NOTE: I am experiencing issues connecting to the DB using docker, please run locally!!!!

## Local
Running locally you need to have PostgreSQL with PostGIS.

First create your virtual env first using Python 3.6. If you run locally, please change the sqlalchemy config
to connect your database.

Run the following commands:
    $ pip install -r requirements.txt
    $ pip install --editable .
    $ magicride db reset

The first command will setup the CLI tool. The other commmand will init and seed the db - this command
can be run on docker too.


Project Structure
-----------------

### Root folder

Folders:

* `app` - This MagicRideAPI implementation is here.
* `cli` - All the CLI commands are listed here. Type `app` in the project root to see all available commands.
* `tests` - These are [pytest](http://pytest.org) tests for this RESTful API
  Server example implementation.

### Application Structure

* `app/__init__.py` - The entrypoint to this Magicride API Server
  application which creates the app and celery as a factory.
* `app/extensions` - All extensions (e.g. SQLAlchemy, etc) are initialized
  here and can be used in the application by importing as, for example,
  `from app.extensions import db`.
* `app/modules` - All endpoints are expected to be implemented here in logically
  separated modules. It is up to you how to draw the line to separate concerns
  (I can create a monolith or microservices with this setup).

Dependencies
------------

### Core Project Dependencies

* [**Python**](https://www.python.org/) 3.6
* [**Flask-Restplus**](https://github.com/noirbizarre/flask-restplus) (+
  [*flask*](http://flask.pocoo.org/))
* [**Marshmallow**](http://marshmallow.rtfd.org/) (+
  [*marshmallow-sqlalchemy*](http://marshmallow-sqlalchemy.rtfd.org/),
  [*flask-marshmallow*](http://flask-marshmallow.rtfd.org/)) - for
  schema definitions. (*supported by the patched Flask-RESTplus*)
* [**GeoAlchemy & SQLAlchemy**]



ENDPOINTS
------------
### Search for all parks w/ filter option
http://localhost:8000/api/v1/parks/ POST
Accepted Parameters:
{
		"filters": {
		"operator": "Six Flags",
		"admission_price": 125,
		"min_height_in_cm": 130,
		"ride_type": ["Animatronic"]
	}
}

### Search for all parks within a path or point w/ filter option
http://0.0.0.0:8000/api/v1/parks/nearest POST
{
	"search": "path",
	"filters": {
		"operator": "Six Flags",
		"admission_price": 125,
		"min_height_in_cm": 130,
		"ride_type": ["Roller Coaster", "Animatronic"]
	},
	"coordinates": [[51.65155, 107.07074],
					[45.0654345, -122.5043534],
					[-16.3200005, -73.577479]],
	"radius": 15
}

OR

{
	"search": "point",
	"latitude": 45.0854345,
	"longitude": -122.5143534,
	"radius": 15
}

### Create a new park
http://0.0.0.0:8000/api/v1/parks/new POST
{
	"name": "Super awesome theme park",
	"latitude": 45.0654345,
	"longitude": -122.5043534,
	"address":"125 fake st",
	"operator": "Disney",
	"opening_time": "10:30",
	"closing_time": "20:00",
	"admission_price": 125,
	"sponsors": ["Pepsi", "Coke"]
}

### Review a ride
(NOTE: If ride or user is not found, it will throw a 404 Not Found)
http://0.0.0.0:8000/api/v1/users/<user_id>/reviews/<ride_id> POST
{
	"description": "if I could ride it everyday, I would!",
	"rating": 5
}

### Get a single park
http://0.0.0.0:8000/api/v1/parks/1 GET

### Create a user
http://0.0.0.0:8000/api/v1/users/ POST
{
	"email": "test@testing.com",
	"password": "verysecretpassword",
	"name": "Mickey Mouse"
}

### Login a user
http://0.0.0.0:8000/api/v1/users/login POST
{
	"email": "test@testing.com",
	"password": "verysecretpassword"
}