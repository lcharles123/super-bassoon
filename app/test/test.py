import unittest
from sys import path
path.append('../')
from app import app, db, Playlist


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Playlist Table', response.data)

    def test_empty_playlist(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No playlists found', response.data)

    def test_populated_playlist(self):
        db.session.add(Playlist(artist_name='Artist 1', track_id='12345'))
        db.session.commit()

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Playlist ID</th>', response.data)
        self.assertIn(b'Artist 1', response.data)
        self.assertIn(b'12345', response.data)

    def test_help_page(self):
        response = self.app.get('/help')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Help', response.data)


if __name__ == '__main__':
    unittest.main()

