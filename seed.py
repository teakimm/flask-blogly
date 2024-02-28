"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()


bob = User(first_name='Bob', last_name="Ross", image_url="https://shorturl.at/bBUX0")


# Add new objects to session, so they'll persist
db.session.add(bob)


# Commit--otherwise, this never gets saved!
db.session.commit()