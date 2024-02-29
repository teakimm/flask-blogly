"""Seed file to make sample data for pets db."""

from models import User, db, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()


bob = User(first_name='Bob', last_name="Ross", image_url="https://shorturl.at/bBUX0")

post1 = Post(title='My first post',
             content='asdfkl;jhasdfgl;khasdfgl;kasdfl;hkasdfghkl',
             user_id=1)
post2 = Post(title='My second post',
             content='!!!!!!!!!!!!!!!!!!',
             user_id=1)

# Add new objects to session, so they'll persist
db.session.add_all([bob, post1, post2])


# Commit--otherwise, this never gets saved!
db.session.commit()