# capstone

##Prerequisties

-Python3.7
-Flask


##APIs

###MOVIES

####GET all MOVIES

You can get all movies by using the `movies` endpoint including the title and the releasedate. You will also get the total number of movies

**example request**

` curl -X GET http://localhost:8080/movies`

**example response**

`{
  "movies": [
    {
      "id": 1, 
      "releasedate": "20.04.1990", 
      "title": "test"
    }, 
    {
      "id": 2, 
      "releasedate": "01.05.1987", 
      "title": "James Bond"
    }
  ], 
  "success": true, 
  "total_movies": 2
}`

##Post Movies

example request `curl -d '{"title":"James Bond", "releasedate":"01.05.1987"}' -H "Content-Type: application/json" -X POST http://localhost:8080/movies`
