**urbandata**

This project was created by Nathan Booth as a development challenge forming part of the interview process for Python Backend Developer at urbanData Analytics.

\
**Challenge**

The goal was to create an authentication service with Django and an HTTP REST API with FastAPI to store, retrieve, and edit properties (inmuebles) from a MongoDB NoSQL database. Only registered users should be able to access the inmuebles endpoints,

\
**Solution overview**

I created two services, authn and inmuebles. authn handles user authentication, using a Django Rest Framework API with a PostgreSQL database. inmuebles allows for CRUD operations on properties, and uses a FastAPI REST API with a MongoDB NoSQL database.

The authn API mainly uses a CustomAuthUser model and related table, which extends Django's built in AbstractUser class.

The inmuebles API mainly uses an inmuebles collection, which has a typed schema defined using pydantic.

I have chosen to focus on the independence of the two services, and at the moment they actually do not communicate directly with each other at all. Given this, a lot of the logic around authentication would happen on the front end.

This is the basic flow of the relationship between the two services:

Essentially, before a user can access any endpoints on the inmuebles service, they must be registered and logged in as a user on the authn service. So from the front end, a user would first register on the authn service, creating a user in the PostgreSQL database. Then the user could log in using email and password with the authn service. The authn service would then issue them a JWT access token and refresh token. To avoid the inmuebles service having to make a request to the authn service with every request that it gets, the inmuebles service simply validates the access token as a dependency on every request. If the user does not pass a valid access token in headers to a request to inmuebles, inmuebles returns a 401 error. For an access token to be valid, it must be signed correctly (the inmuebles service uses the same secret key to validate the token as the authn service uses to create the token) and not be expired. The access token expires every several minutes, at which point the user passes the refresh token (which takes longer to expire) to the authn server, and is given a new access token and a new refresh token. If the user does not use the app for some days, both tokens will have expired and they will have to log in again, thus receiving new tokens. The front end would handle calling authn for new tokens every time it gets a 401 error for an invalid token from the inmuebles service.

The authn service uses the Django Rest Framework library to create REST API endpoints and another library built on top of it called Simple JWT to create and manage access and refresh tokens, as well as handle login.

The inmuebles service uses FastAPI with a MongoDB database called "inmueble," hosted on Atlas. The collection is called "inmuebles." There is a Python migration script to import inmuebles from a CSV into the database, which does cleaning of the types of issues that were seen in the sample CSV.

Right now, we have not considered authorization: all registered users are allowed to access all endpoints.

There is a very small amount of test coverage, mostly for the access token checks in inmuebles.

\
**Important authn endpoints**

_POST /authn/register/ takes fields as body, creates a new CustomAuthUser in the database, returns CustomAuthUser_

_POST /authn/token/ This is the login endpoint. Takes username and password as fields, and returns an auth token and a refresh token_

_POST /authn/token/refresh This endpoint refreshes the access token and refresh token if the refresh token is still valid. It takes those tokens as the body, and returns an auth token and a refresh token_

\
**Important inmuebles endpoints**

All of these call validate\_token as a dependency, so all requests need access-token.

_GET /inmuebles/ returns a list of all inmuebles from the database_

_POST /inmuebles/ creates a new inmueble document in the database; body has Inmueble object; returns Inmueble object created_

_PUT /inmuebles/{id} edits an inmueble document in the database, but cannot change ID; gets inmueble by id, a string; body has Inmueble object; returns Inmueble object post edit_

_GET /inmuebles/{id} gets an inmueble document from the database by id, a string; returns an Inmueble object_

_DELETE /inmuebles/{id} deltes an inmueble document from the database by id, a string; returns status code_

For more specific documentation for the inmuebles API endpoints, once the server is running, go to [http://0.0.0.0/docs](http://0.0.0.0/docs)

\
**authn Installation**

You must have Python 3, pip, PostgreSQL, and pyenv installed.

To install the authn service, run the following commands:

_pyenv virtualenv 3.10.6 urbandata\_env_

_pyenv activate urbandata\_env_

_pip install -r requirements.txt_

_pg\_ctl -D /usr/local/var/postgresql\@14 start && brew services start postgresql_

_psql postgres_

Inside of psql:

_create database users;_

_CREATE USER django\_user WITH PASSWORD 'massiveeducatedbuffalo';_

_GRANT ALL PRIVILEGES ON DATABASE users TO django\_user;_

_ALTER ROLE django\_user SET client\_encoding TO 'utf8';_

_ALTER ROLE django\_user SET default\_transaction\_isolation TO 'read committed';_

_ALTER ROLE django\_user SET timezone TO 'UTC';brew install mongodb-community@6.0_

_ALTER USER django CREATEDB;_

Back in terminal:

_python manage.py makemigrations_

_python manage.py migrate_

\
**authn Use**

To start the PostgreSQL server:

_pg\_ctl -D /usr/local/var/postgresql\@14 start_

To run the service, from urbandata/uda\_auth\_app/uda\_auth:

_python manage.py runserver_

To run tests for authn, from urbandata/uda\_auth\_app/uda\_auth:

_python manage.py test_

\
**inmuebles Installation**

You must have Docker installed.

Run the following commands:

_docker pull nategbooth/inmuebles\_image_

\
**inmuebles Use**

To run the service:

_docker run -d --name inmueblescontainer -p 80:80 nategbooth/inmuebles\_image_

You can test it using automatically generated forms in [http://0.0.0.0/docs](http://0.0.0.0/docs)

To run tests for inmuebles:

There are just a few and I didn't have a chance to set them up to work with Docker, they worked well while testing locally but they require some libraries be installed. They lightly test the access token checking. They are in inmuebles\_app/inmuebles/test\_all.py

\
**Steps taken**

Normally I would have started with the inmuebles service, and for both of the services I would have created tests for various cases first (with TDD in mind). However, I was trying to more or less follow the order the tasks were presented in the challenge.

My steps were, roughly:

Decide architecture and figure out questions

Create list of more or less well-defined tasks

Define endpoints

Set up framework of authn service

Create User model to be used for authn service

Set up PostgreSQL database

Set up MongoDB Atlas

Create script for parsing assets.csv and inserting inmuebles in the database

Create FastAPI app with CRUD functionality

Set up endpoints in authn for issuing and updating access and refresh tokens

Added access token checking for all endpoints in inmuebles service using a dependency, and create tests for its basic functionality

Set up Docker for inmuebles service

Wrote README

\
**Difficulties**

The conceptual and design difficulty of this project was fairly low. Of course it would be possible to think of more "best practice" or efficient ways to do many of these tasks, but that was not the main goal of the challenge. The main difficulties came from implementing all of these technologies from scratch, especially because this was the first time I was using Django, FastAPI, MongoDB, or Docker. In particular, combining these and other technologies was sticky in some moments. Overall, the amount of time spent coding was quite short (the inmuebles API only took about a half an hour to create the basic functionality); most of the time was spent reading documentation and debugging. In particular, since some of these technologies (particularly Django) are so widely used, there does not see to always be a well-agreed-upon "best" way of doing things, so a good amount of time was dedicated to deciding which way seemed clearest or easiest for the challenge.

Here are some points where I got particularly stuck:

Passwords were being hashed because of the way the model was being saved

Having trouble installing PostgreSQL in a Docker container with Python

Imports of my modules broke when I started using Docker, and it was hard to get it to work both locally outside of docker and in Docker.

Kept thinking something was wrong with the API when I passed up "access\_token" instead of "access-token" and it failed.

\
**Ways to improve**

Since this was written quickly and just as a challenge, not intended to be run on a production server, there are innumerable ways it could be improved.

Here are some aspects that would need to be changed if this were to be run in production:

More test coverage. I am sure there are bugs I haven't noticed yet, I have mainly been testing with a request generating and sending tool called Postman, as well as the automatically generated forms in /docs for FastAPI. Testing should also be done before every commit.

Add a filter endpoint that lets users filter inmuebles by a custom selection of parameters.

More field validation, make sure users cannot create invalid states

Include authorization: all users should probably not be allowed to delete any inmueble

Containerize authn app

Flesh out the admin page in Django to be able to handle superusers

Set up structures so internationalization/localization will be possible later without too much extra work.

Make tests run automatically.

Set up development/deployment processes to prevent errors from going into production

Make it possible for users to change passwords.

Create sign\_out backend

Run tests within Docker.

Make README more concise.

\
**Shortcuts taken/aspects not being considered**

Aspects I was not considering more or less at all (there are more, but this is a sampling):

Efficiency

Data validation -- for example, something like build\_status for an inmueble could probably be an Enum.

Versioning

Tracking dependencies

Creating views

Security -- I am not throttling account creating calls, for example.

Did not consider thoroughly what fields could be useful in user model or other domain-specific questions

In the CSV parsing script, did not consider other data cleaning issues aside from the ones evident in assets.csv

I did not do much validation of fields at all

Did not thoroughly consider MongoDB schema, for example to optimize for space by having null fields not be included in the document.

Hardcoded certain strings including secret key

Could have been better to do asymmetric token encryption so that the two services don't have to share a secret key

I just assumed that id\_uda in assets.csv is the real ID from the database, because of the name, and because the other ID field would be weird because it's in quotes in one row. However, I am unclear where the CSV came from so that would affect how to parse it.

I decided not to allow partial updates to edit inmuebles because so far the front end would always have the full object while editing.

I split x coordinates and y coordinates, but I am unsure if that is good practice.

I left in some unused code because of time constraints.

I didn't worry too much about the Docker configuration.

\
**What I would do differently**

I wish I had spent less time reading documentation trying to figure out the right way to do things and just done some parts whichever way at the start. I wish I had set up Docker from the beginning. I also would have done the whole process more incrementally, starting out with barebones versions of each service. If testing had not been optional, I would normally write many of the tests before writing endpoints. I think TDD is an effective way of making sure functions behave as desired.