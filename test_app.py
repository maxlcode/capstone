import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.assistent_token = os.environ['assistent_token']
        self.director_token = os.environ['director_token']
        self.producer_token = os.environ['producer_token']
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            'title':'James Bond 007', 
            'releasedate':'2020-05-23',
        }

        self.wrong_data_format_new_movie = {
            'releasedate':'24924925sqwer5',
        }

        self.new_actor = {
            'name':'Daniel Craig',
            'age': 56,
            'gender': 'male'
        }

        self.wrong_data_format_new_actor = {
            'name':'Daniel Craig',
            'age': 'MF§4i2',
            'gender': 'male'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            #self.db_drop_and_create_all()
            self.client().post('/movies', json=self.new_movie,
                headers={'Authorization': "Bearer {}".format(self.producer_token)
                })
            self.client().post('/actors', json=self.new_actor,
                headers={'Authorization': "Bearer {}".format(self.producer_token)
                })

    def tearDown(self):
        """Executed after reach test"""
        pass

    #TESTS FOR GET/MOVIES ENDPOINT
    
    def test_get_movies_no_role(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_movies_assistent(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_get_movies_director(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_get_movies_producer(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    #TESTS FOR GET/MOVIES/<movie_ID> ENDPOINT

    def test_get_specific_movies_no_role(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_specific_movies_assistent(self):
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_get_specific_movies_director(self):
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_get_specific_movies_producer(self):
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_get_specific_movies_producer(self):
        res = self.client().get('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #TESTS FOR POST /MOVIES  ENDPOINT
    def test_post_movie_no_role(self):
        res = self.client().post('/movies',json=self.new_movie )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_post_movie_assistent(self):
        res = self.client().post('/movies', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'], 'unauthorized')
        
    def test_post_movie_director(self):
        res = self.client().post('/movies', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
    
    def test_post_movie_producer(self):
        res = self.client().post('/movies', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['created'],True)

    def test_post_invalid_new_movie_format(self):
        res = self.client().post('/movies', json=self.wrong_data_format_new_movie,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'unprocessable')

 #TESTS FOR PATCH /MOVIES  ENDPOINT

    def test_patch_movie_no_role(self):
        res = self.client().patch('/movies/1',json=self.new_movie )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_patch_movie_assistent(self):
        res = self.client().patch('/movies/1', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'], 'unauthorized')
        
    def test_patch_movie_director(self):
        res = self.client().patch('/movies/1', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['id'],True)
    
    def test_post_movie_producer(self):
        res = self.client().patch('/movies/1', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['id'],True)
    
    def test_patch_invalid_new_movie_format(self):
        res = self.client().patch('/movies/1', json=self.wrong_data_format_new_movie,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_patch_not_existing_movie(self):
        res = self.client().patch('/movies/500', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')
    
    #TESTS FOR DELETE /MOVIES  ENDPOINT

    def test_delete_movie_no_role_not_authorized(self):
        res = self.client().delete('/movies/2',json=self.new_movie )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_assistent_no_permission(self):
        res = self.client().delete('/movies/2', 
            headers={'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'], 'unauthorized')
        
    def test_delete_movie_director_no_permission(self):
        res = self.client().delete('/movies/2', 
            headers={'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNotNone(data['error'], 'unauthorized')
    
    def test_delete_movie_producer_successful(self):
        res = self.client().post('/movies', json=self.new_movie,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        res = self.client().delete('/movies/'+str(data['created']),
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['deleted'],True)

    def test_delete_not_existing_movie(self):
        res = self.client().delete('/movies/500',
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    
    #----------------------------------------------
    #----------------- ACTORS TESTS ---------------
    #----------------------------------------------

    # TESTS FOR GET /ACTORS  ENDPOINT
    def test_get_actors_no_role(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_actors_assistent(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_get_actors_director(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_get_actors_producer(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    #TESTS FOR GET/Actors/<actors_ID> ENDPOINT

    def test_get_specific_actors_no_role(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_specific_actors_assistent(self):
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_get_specific_actors_director(self):
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_get_specific_actors_producer(self):
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_get_specific_actors_producer(self):
        res = self.client().get('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    #TESTS FOR POST /actors ENDPOINT
    def test_post_actor_no_role(self):
        res = self.client().post('/actors',json=self.new_actor )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_post_actor_assistent(self):
        res = self.client().post('/actors', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'], 'unauthorized')
        
    def test_post_actor_director(self):
        res = self.client().post('/actors', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['created'],True)
    
    def test_post_actor_producer(self):
        res = self.client().post('/actors', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['created'],True)
    
    def test_post_invalid_new_actor_format(self):
        res = self.client().post('/actors',
            json=self.wrong_data_format_new_actor,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'unprocessable')
    
 #TESTS FOR PATCH /actors  ENDPOINT

    def test_patch_actor_no_role(self):
        res = self.client().patch('/actors/1',json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_patch_actor_assistent(self):
        res = self.client().patch('/actors/1', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'], 'unauthorized')
        
    def test_patch_actor_director(self):
        res = self.client().patch('/actors/1', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['id'],True)
    
    def test_post_actor_producer(self):
        res = self.client().patch('/actors/1', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['id'],True)
    
    def test_patch_invalid_new_actor_format(self):
        res = self.client().patch('/actors/1', 
            json=self.wrong_data_format_new_actor,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_patch_not_existing_actor(self):
        res = self.client().patch('/actors/500', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')
    
    #TESTS FOR DELETE /actors  ENDPOINT

    def test_delete_actor_no_role_not_authorized(self):
        res = self.client().delete('/actors/2' )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_delete_actor_assistent_no_permission(self):
        res = self.client().delete('/actors/2', 
            headers={'Authorization': "Bearer {}".format(self.assistent_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'], 'unauthorized')
       
    def test_delete_actor_director_permission(self):
        res = self.client().post('/actors', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        res = self.client().delete('/actors/'+str(data['created']),
            headers={'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['deleted'],True)       
    
    def test_delete_actor_producer_successful(self):
        res = self.client().post('/actors', json=self.new_actor,
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        res = self.client().delete('/actors/'+str(data['created']),
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertIsNotNone(data['deleted'],True)
    
    def test_delete_not_existing_actor(self):
        res = self.client().delete('/actors/500',
            headers={'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()