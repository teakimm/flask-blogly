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

    posts = db.relationship(
        'Post', secondary='posts_tags', backref='tags'
    )


class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    # can specify multi-column unique or check constraints like:
    # __table_args__ = (
    #    db.UniqueConstraint("col1", "col2"),
    #    db.CheckConstraint("born <= died")

    __table_args__ = db.UniqueConstraint("post_id", "tag_id"),

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

# bob = User(first_name='Bob', last_name="Ross", image_url="https://shorturl.at/bBUX0")

# post1 = Post(title='My first post',
#              content='asdfkl;jhasdfgl;khasdfgl;kasdfl;hkasdfghkl',
#              user_id=1)

# tag1 = Tag (id=1, name='Funny')

# post_tag1 = PostTag(post_id=1, tag_id=1)