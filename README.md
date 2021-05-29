# Capstone

This is a project to test the skills learned during the udacity nanodegree programm
The idea is to have a application which is storing movies and actors a database.
There are different roles which can different CRUD actions on that data
The data can be accessed via APIs. The authentication is done via Auth0

## Getting started

The application can either be access on `https://capstone-maxlcode.herokuapp.com/`
or on the `http://localhost:8080/` if it is deployed locally


## Prerequisties for local deployment

- Python3.7
- pip (python package manager)
- Flask
- postgres 13.0

Is it recommended to create a local virtual environment. Please see [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

After virtual environment is created and activated, make sure to install dependencies with `pip install -r requirements.txt`

Make sure to run the 'setup.sh' bash file in order to set all relevant environment variables 

Also export tell the system where your flask app is located:

`export FLASK_APP=app.py`

Finally run the app
`python app.py`

## APIs

### Authorization
Authorization is done via Auth0.com using a bearer token. 

### RBAC

Role Based Access Control is implemented for all APIs (only the `/`(heartbeat) does not have one)

**Casting Assistant**
- Can view actors and movies
-->`read:movies`,`read:actors`
**Casting Director**
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
--> `create:actors`,`delete:actors`,`read:actors`,`update:actors`,`read:movies`,`update:movies`
**Executive Producer**
- All permissions a Casting Director has and…
- Add or delete a movie from the database
--> `create:actors`,`delete:actors`,`read:actors`,`update:actors`,`read:movies`,`update:movies`,`post:movies`,`delete:movies`,

When using the APIs please make sure you use the right token in the header with the needed permissions to perform actions.

### MOVIES

#### GET all MOVIES

You can get all movies by using the `movies` endpoint including the title and the releasedate. You will also get the total number of movies

**example response**
```json
{
  "movies": [
    {
      "id": 1, 
      "releasedate": "1926-03-31", 
      "title": "Terminator"
    }, 
    {
      "id": 2, 
      "releasedate": "1987-05-01", 
      "title": "James Bond"
    }
  ], 
  "success": true, 
  "total_movies": 2
}
```

#### GET a specific movie

You can get a specific movie by using the `movies/<movie-id>` endpoint with a `GET`. You will get the id, the title and the releasedate.

**example response**
```json
{
    "id": 1,
    "releasedate": "Tue, 01 Jan 1985 00:00:00 GMT",
    "success": true,
    "title": "James Bond"
}
```

#### POST Movies

You can create a new movie using the `POST` method with the `movies` endpoint

**example request data**
```json
{
    "title":"Chuck Norris",
    "releasedate": "1957-06-12"
}
```

**example response**
```json
{
    "created": 4,
    "success": true
}
```

#### UPDATE Movies

You can update a new movie using the `PATCH` method with the `movies` endpoint

**example request**

```json
{
    "title":"Indiana Jones",
    "releasedate": "1974-04-06"  
}
```


**example response**
```json
{
    "id": 2,
    "releasedate": "Sat, 06 Apr 1974 00:00:00 GMT",
    "success": true,
    "title": "Indiana Jones"
}
```

#### DELETE Movies

This endpoint can be used to delete a specific movie. Therefore a `DELETE` request must be send to the `movies\<movie_id>` endpoint


**example response**
{
    "deleted": 2,
    "success": true
}


### ACTORS

#### GET all Actors

You can get all actors including the name, age and the gender by using the `actors` endpoint . You will also get the total number of actors

**example response**
```json
{
    "actors": [
        {
            "age": "Daniel Craig",
            "gender": "male",
            "id": 1,
            "name": "Daniel Craig"
        }
    ],
    "success": true,
    "total_actors": 1
}
```

#### GET a specific actor

You can get a specific actor by using the `actors/<actor-id>` endpoint with a `GET`. You will get the id, the nane, the age and the gender.

**example response**
```json
{
    "age": 46,
    "gender": "male",
    "id": 1,
    "name": "Daniel Craig",
    "success": true
}
```

#### POST Actors

You can create a new actor using the `POST` method with the `actors` endpoint

**example request data**
```json
{
    "name":"Daniel Craig",
    "age": 46,
    "gender": "male"
}
```

**example response**
```json
{
    "created": 4,
    "success": true
}
```

#### UPDATE Actors

You can update a new actor using the `PATCH` method with the `actors` endpoint

**example request**

```json
{
    "name":"Daniel Radcliffe",
    "age": 23,
    "gender": "male"
}
```


**example response**
```json
{
    "age": 23,
    "gender": "male",
    "id": 3,
    "name": "Daniel Radcliffe",
    "success": true
}
```

#### DELETE Actors

This endpoint can be used to delete a specific actor. Therefore a `DELETE` request must be send to the `actors\<actor_id>` endpoint


**example response**
{
    "deleted": 2,
    "success": true
}

## TESTING

### Unittest

Unittest can be performed with the `test_app.py' file.

Please make sure you export the tokens
`export assistent_token=<token>`
`export director_token=<token>`
`export producer_token=<token>`

Then run the file by the command `python test_app.py`

### Testing Deployment

For testing the deployment on `https://capstone-maxlcode.herokuapp.com/` please feel free to use postman collection. 
It may be needed to update the token if they are expired