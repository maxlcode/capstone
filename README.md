# capstone

## Prerequisties

<<<<<<< HEAD
- Python3.7
- Flask
=======
-Python3.7
-Flask
>>>>>>> 1ec33803e3b4920df3a1846ad315edf57bebad4b


## APIs

### MOVIES

#### GET all MOVIES

You can get all movies by using the `movies` endpoint including the title and the releasedate. You will also get the total number of movies

**example request**

` curl -X GET http://localhost:8080/movies`

**example response**
<<<<<<< HEAD
```json
{
  "movies": [
    {
      "id": 1, 
      "releasedate": "23.05.1957", 
      "title": "Terminator"
=======

`{
  "movies": [
    {
      "id": 1, 
      "releasedate": "20.04.1990", 
      "title": "test"
>>>>>>> 1ec33803e3b4920df3a1846ad315edf57bebad4b
    }, 
    {
      "id": 2, 
      "releasedate": "01.05.1987", 
      "title": "James Bond"
    }
  ], 
  "success": true, 
  "total_movies": 2
<<<<<<< HEAD
}
```

## GET a specific movie

## POST Movies

**example request**

`curl -d '{"title":"James Bond", "releasedate":"01.05.1987"}' -H "Content-Type: application/json" -X POST http://localhost:8080/movies`

## UPDATE Movies

This endpoint can be used to delete a specific movie. Therefore a UPDATE request must be send to the `movies\<movie_id>` endpoint

**example request**

`curl -d '{"title":"Arnold Schwarzenegger", "releasedate":"05.05.2021"}' -H "Content-Type: application/json" -X PATCH http://localhost:8080/movies/1`

**example response**
```json
{
  "id": 1,
  "releasedate": "Wed, 05 May 2021 00:00:00 GMT",
  "success": true,
  "title": "Terminator"
}
```

## DELETE Movies

This endpoint can be used to delete a specific movie. Therefore a DELETE request must be send to the `movies\<movie_id>` endpoint

**example request** 
`curl -H "Content-Type: application/json" -X DELETE http://localhost:8080/movies/1`

**example response**

```json
{
  "deleted": 1,
  "success": true
}
```
=======
}`

## Post Movies

example request `curl -d '{"title":"James Bond", "releasedate":"01.05.1987"}' -H "Content-Type: application/json" -X POST http://localhost:8080/movies`
>>>>>>> 1ec33803e3b4920df3a1846ad315edf57bebad4b
