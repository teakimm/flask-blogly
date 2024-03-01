from unittest import TestCase
from models import DEFAULT_IMAGE_URL, User, Post
from app import app, db
import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"
# import app first before models

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
print("***************************", app.config['SQLALCHEMY_DATABASE_URI'])
# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None
        )

        db.session.add(test_user)

        db.session.commit()

        test_post = Post(
            title="Hello World",
            content="This is a test post.",
            user_id=test_user.id
        )

        db.session.add(test_post)

        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        ''' Tests if users are rendered correctly '''
        with app.test_client() as client:

            resp = client.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_new_user_form(self):
        ''' Tests if new user is correctly added and rendered '''
        with app.test_client() as client:
            resp = client.post(
                "/users/new",
                data={'first_name': "Bruce",
                      "last_name": "Willis",
                      "image_url": ""
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Bruce Willis", html)

    def test_delete_user(self):
        ''' Tests if user was deleted correctly '''
        with app.test_client() as client:
            # can just assign this as resp
            resp = client.post(
                f'/users/{self.user_id}/delete',
                follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertIn(f"test1_first test1_last has been", html)

    def test_user_profile(self):
        ''' Tests if user profile is correctly rendered '''
        with app.test_client() as client:
            resp = client.get(
                f'/users/{self.user_id}',
            )

            html = resp.get_data(as_text=True)

            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)
            self.assertIn("<!-- Test working -->", html)

    def test_incorrect_user_route(self):
        """Tests if correct response code is given if invalid route for user"""
        with app.test_client() as client:

            resp = client.get("/users/9999")
            self.assertEqual(resp.status_code, 404)
    #add these to a new class
    def test_delete_post(self):
        """Tests if post is deleted and flash message is shown"""
        with app.test_client() as client:
            resp = client.post(
                f'/posts/{self.post_id}/delete',
                follow_redirects=True
            )
        html = resp.get_data(as_text=True)
        self.assertIn(f"Hello World has been deleted successfully", html)

    def test_render_add_post_form(self):
        """Tests if the post form html is rendered correctly"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<!-- this is to test new post form -->", html)

    def test_add_post(self):
        """Tests if form data for post is correctly submitted and rendered"""
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/posts/new",
                data={'title': "Test title, please ignore",
                      "content": "This is the content of test title"
                      },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test title, please ignore", html)

    def test_edit_post(self):
        """Tests if editing a post is correctly submitted and rendered"""
        with app.test_client() as client:
            resp = client.post(
                f'/posts/{self.post_id}/edit',
                data={
                    "title": "we are editing this title",
                    "content": "also the content is changed"
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("we are editing this title", html)

    def test_incorrect_post_route(self):
        """Tests if inputting an invalid route for a posts gives the intended
        response code.
        """
        with app.test_client() as client:

            resp = client.get("/posts/9093019")
            self.assertEqual(resp.status_code, 404)
