# Casting Agency API

## Capstone Project for Udacity's Full Stack Developer Nanodegree
Heroku Link: https://udacity-final-project-fsnd.herokuapp.com/


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

## Running the server

Before running the application locally, make sure to change `database_url` in `models.py`
To run the server, execute:

1. Run `setup.sh`, where authentications live.
2. Execute:
```bash
python app.py
```
## API Reference

## Getting Started
Base URL: This application can be run locally. The hosted version is at `https://ry-fsnd-capstone.herokuapp.com`.

Authentication: This application requires authentication to perform various actions. All the endpoints require
various permissions, except the root (or health) endpoint, that are passed via the `Bearer` token.

The application has three different types of roles, check `setup.sh` for JWT keys:
- User
  - can only view the list of actors and movies.
- Manager
  - can perform all the actions that `User` can
  - can also create an actor and movie and also update respective information
  - has `patch:actor, patch:movie, post:actor, post:movie` permissions
- Admin
  - can perform all the actions that `Manager` can
  - can also delete an actor or a movie
  - has `delete:actor, delete:movie` permissions in addition to all the permissions that `Manager` role has


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": false
    "error": error.code,
    "message": error.message,
}
```

The API will return the following errors based on how the request fails:
 - 400: Bad Request
 - 401: Unauthorized
 - 404: Not Found
 - 422: Unprocessable Entity
 - 500: Internal Server Error

## Endpoints

#### GET /
 - General
   - root endpoint
   - can also work to check if the api is up and running
   - is a public endpoint, requires no authentication

Sample Response
```
Hello, World
```

#### GET /actors
 - General
   - gets the list of all the actors
 
Sample Response
```
{
   "actors":[
      {
         "age":"12",
         "gender":"male",
         "id":1,
         "name":"test"
      }
   ],
   "success":true
}
```


#### POST /actors
 - General
   - creates a new actor
   - requires `post:actor` permission
 
 - Request Body (json)
   - name: string
   - gender: string
   - age: string
 

Sample Response
```
{
    "actor": {
        "age": "45",
        "gender": "male",
        "id": 2,
        "name": "test2"
    },
    "success": true
}
```

#### PATCH /actors/{actor_id}
 - General
   - updates the info for an actor
   - requires `patch:actor` permission
 
 - Request Body (json)
   - name: string
   - gender: string
   - age: string
 

Sample Response
```
{
    "actor": {
        "age": "45",
        "gender": "male",
        "id": 2,
        "name": "test2"
    },
    "success": true
}
```

#### DELETE /actors/{actor_id}
 - General
   - deletes the actor
   - requires `delete:actor` permission
   - will also delete the mapping to the movie but will not delete the movie from the database
 
Sample Response
```
{
    "success": true,
    "actor_id": 2
}
```

#### GET /movies
 - General
   - gets the list of all the movies
   - requires `get:movies` permission
 
Sample Response
```
{
   "movies":[
      {
         "id":1,
         "release":"2020",
         "title":"Avengers"
      }
   ],
   "success":true
}
```

#### POST /movies
 - General
   - creates a new movie
   - requires `post:movie` permission
 
 - Request Body
   - title: string
   - release: string

Sample Response
```
{
    "movie": {
        "id": 2,
        "release": "2010",
        "title": "Avengers 2"
    },
    "success": true
}
```

#### PATCH /movie/{movie_id}
 - General
   - updates the info for a movie
   - requires `patch:movie` permission
 
 - Request Body
   - title: string
   - release: string

Sample Response
```
{
    "movie": {
        "id": 2,
        "release": "2010",
        "title": "Avengers 2"
    },
    "success": true
}
```

#### DELETE /movies/{movie_id}
 - General
   - deletes the movie
   - requires `delete:movie` permission
   - will not affect the actors present in the database

```
{
    "success": true,
    "movie_id": 2
}
```