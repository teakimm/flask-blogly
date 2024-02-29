"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://shorturl.at/lrFV6"

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    first_name = db.Column(
        db.Text,
        nullable = False,
    )

    last_name = db.Column(
        db.Text,
        nullable = False,
    )

    image_url = db.Column(
        db.Text,
        nullable = False,
        default = DEFAULT_IMAGE_URL
    )
