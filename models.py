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
    ''' Blueprint for user table '''
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
    posts = db.relationship("Post", backref="user")


class Post(db.Model):
    """Blueprint for post table"""

    __tablename__ = "posts"


    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    title = db.Column(
        db.String(75),
        nullable = False,
    )

    content = db.Column(
        db.Text,
        nullable = False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable = False
    )

    tags = db.relationship(
        'Tag', secondary='posts_tags', backref='posts'
    )

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    name = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )


class PostTag(db.Model):

    __tablename__ = 'posts_tags'


    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )

