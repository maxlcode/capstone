import os
import sys
import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors, db_drop_and_create_all
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  db_drop_and_create_all()

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 
      'Content-Type,Authorization,true'
      )
    response.headers.add(
      'Access-Control-Allow-Methods', 
      'GET,PUT,POST,DELETE,OPTIONS'
      )
    return response

  # heartbeat to check if app is up and running
  @app.route('/')
  def heartbeat():
        return jsonify({'message': 'Application is running'}), 200
  #----------------------------------------------
  #--------------MOVIE ENDPOINTS-----------------
  #----------------------------------------------

  # GET Movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('read:movies')
  def get_all_movies(payload):
    movies =  Movies.query.all()

    return jsonify({
      'success': True,
      'movies': [movie.format() for movie in movies],
      'total_movies':len(movies),
    })

  # GET a specific movie
  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth('read:movies')
  def get_movie(payload, movie_id):
    # look if movie id is existing
    movie = Movies.query.filter(
                  Movies.id == movie_id).one_or_none()
    #if not existing - 404 error
    if movie is None:
      abort(404)

    try:  
      return jsonify({
        'success': True,
        'id': movie.id,
        'title': movie.title,
        'releasedate': movie.releasedate
      })

    except Exception as e:
      print(e)
      abort(422)

  # POST new movies
  @app.route('/movies', methods=['POST'])
  @requires_auth('create:movies')
  def create_movie(payload):
    try:
      body = request.get_json()
      new_title = body.get('title', None)
      new_releasedate = body.get('releasedate', None)

      if new_title is None:
        #print('title not existing', file=sys.stderr)
        abort(422)

      if new_releasedate is None:
        #print('new_releasedate not existing', file=sys.stderr)
        abort(422)

    except Exception as e:
      print(e)
      abort(422)
    #check 
    try: 
      test= datetime.datetime.strptime(new_releasedate, '%Y-%m-%d')
    except:
      abort(422)


    try:
      new_movie = Movies(title=new_title, 
                            releasedate=new_releasedate, 
                            )
      new_movie.insert()

      return jsonify({
        'success': True,
        'created': new_movie.id,
      })

    except Exception as e:
      print(e)
      abort(422)

  #Update an existing movie
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('update:movies')
  def update_movie(payload, movie_id):
      body = request.get_json()
      new_title = body.get('title', None)
      new_releasedate = body.get('releasedate', None)

      if new_title is None:
        #print('title not existing', file=sys.stderr)
        abort(422)

      if new_releasedate is None:
        #print('new_releasedate not existing', file=sys.stderr)
        abort(422)

      try: 
        test= datetime.datetime.strptime(body['releasedate'], '%Y-%m-%d')
      except:
        #print('date wrong format', file=sys.stderr)
        abort(422)

      try:
        movie_to_update = Movies.query.filter(Movies.id == movie_id).one_or_none()
      except:
        #print('movie_to_update not existing', file=sys.stderr)
        abort(404)

      #if not existing - 404 error
      if movie_to_update is None:
        #print('movie not existing', file=sys.stderr)
        abort(404)

      # check if title or releasedate has changed, otherwise keep old one
      try:
          movie_to_update.title= body['title'] 
      except: 
          movie_to_update.title = movie_to_update.title
      try:
          movie_to_update.releasedate= body['releasedate'] 
      except: 
          movie_to_update.releasedate = movie_to_update.releasedate

      #finally update
      try:
          movie_to_update.update()
          return jsonify({
              'success': True,
              'id': movie_id,
              'title': movie_to_update.title,
              'releasedate': movie_to_update.releasedate,
          })
      except Exception as e:
          print(e)
          abort(422)

  #DELETE an existing movie
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):

    # look if id is existing
    
    movie = Movies.query.filter(
                  Movies.id == movie_id).one_or_none()
    #if not existing - 404 error
    if movie is None:
      abort(404)
    try:
    #delete from db
      movie.delete()
    
      return jsonify({
        'success': True,
        'deleted': movie_id,
      })

    except Exception as e:
      print(e)
      abort(422)

  #----------------------------------------------
  #--------------ACTORS ENDPOINTS-----------------
  #----------------------------------------------

  # GET Actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('read:actors')
  def get_all_actors(payload):
    actors =  Actors.query.all()

    return jsonify({
      'success': True,
      'actors': [actor.format() for actor in actors],
      'total_actors':len(actors),
    })

  # GET a specific movie
  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('read:actors')
  def get_actor(payload, actor_id):
    # look if actor id is existing
    
    actor = Actors.query.filter(
                  Actors.id == actor_id).one_or_none()
    #if not existing - 404 error
    if actor is None:
      abort(404)

    try:  
      return jsonify({
        'success': True,
        'id': actor.id,
        'name': actor.name,
        'age': actor.age,
        'gender': actor.gender,
      })

    except Exception as e:
      print(e)
      abort(422)

  # POST new movies
  @app.route('/actors', methods=['POST'])
  @requires_auth('create:actors')
  def create_actor(payload):
    try:
      body = request.get_json()
      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)
      if new_name is None:
        #print('new name not existing', file=sys.stderr)
        abort(422)

      if new_age is None or not isinstance(new_age, int):
        #print('new age not existing', file=sys.stderr)
        abort(422)

      if new_gender is None:
          #print('new gender not existing', file=sys.stderr)
          abort(422)

    except Exception as e:
      print(e)
      abort(422)

    try:
      new_actor = Actors(name=new_name, 
                            age=new_age,
                            gender = new_gender 
                            )
      new_actor.insert()

      return jsonify({
        'success': True,
        'created': new_actor.id,
      })

    except Exception as e:
      print(e)
      abort(422)

  #Update an existing actor
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('update:actors')
  def update_actor(payload, actor_id):
      body = request.get_json()
      new_name = body.get('name', None)
      new_age= body.get('age', None)
      new_gender = body.get('gender', None)


      if new_name is None:
        #print('new name not existing', file=sys.stderr)
        abort(422)

      if new_age is None or not isinstance(new_age, int):
        #print('new age not existing', file=sys.stderr)
        abort(422)

      if new_gender is None:
          #print('new gender not existing', file=sys.stderr)
          abort(422)

      try:
        actor_to_update = Actors.query.filter(Actors.id == actor_id).one_or_none()
      except:
        abort(404)

      #if not existing - 404 error
      if actor_to_update is None:
          abort(404)
      
      # check if title or releasedate has changed, otherwise keep old one
      try:
          actor_to_update.name= body['name'] 
      except: 
          actor_to_update.name = actor_to_update.name
      try:
          actor_to_update.age= body['age'] 
      except: 
          actor_to_update.age = actor_to_update.age
      try:
          actor_to_update.gender= body['gender'] 
      except: 
          actor_to_update.gender = actor_to_update.gender


      try:
          actor_to_update.update()
          return jsonify({
              'success': True,
              'id': actor_id,
              'name': actor_to_update.name,
              'age': actor_to_update.age,
              'gender': actor_to_update.gender,
          })
      except Exception as e:
          print(e)
          abort(422)
          
  #DELETE an existing movie
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
    # look if id is existing
    
    actor = Actors.query.filter(
                    Actors.id == actor_id).one_or_none()
    #if not existing - 404 error
    if actor is None:
      abort(404)
      #delete from db
    try:
      actor.delete()
      return jsonify({
        'success': True,
        'deleted': actor_id,
      })

    except Exception as e:
      print(e)
      abort(422)



  #----------------------------------------------
  #--------------ERROR-HANLDERS------------------
  #----------------------------------------------

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  @app.errorhandler(AuthError)
  def auth_error(error):
    #print(error.status_code, file=sys.stderr)
    #print(error.error['description'], file=sys.stderr)
    return jsonify({
      "success": False,
      "error": error.error['code'],
      "message": error.error['description']
      }), error.status_code

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)