"""Seed file to make sample data for pets db."""

from models import User, db, Post, Tag, PostTag
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

tag1 = Tag (id=1, name='Funny')



# Add new objects to session, so they'll persist
db.session.add_all([bob, post1, post2, tag1])
db.session.commit()

post_tag1 = PostTag(post_id=1, tag_id=1)

db.session.add(post_tag1)
db.session.commit()

# Commit--otherwise, this never gets saved!