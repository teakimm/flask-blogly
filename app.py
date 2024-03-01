"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request, flash, session
from models import connect_db, User, Post, db, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get("/")
# just call homepage, name indicates what should be displayed
def users_redirect():
    ''' Redirects to users page '''
    return redirect("/users")


@app.get("/users")
def render_user_page():
    ''' Renders users page '''
    # when querying for all, make sure to order by
    users = User.query.all()

    return render_template("users_list.html", users=users)


@app.get("/users/new")
def render_new_user_form():
    ''' Renders new user form '''
    return render_template("new_user_form.html")


@app.post('/users/new')
def add_user():
    ''' Adds user and redirects to users page '''
    form_data = request.form
    first_name = form_data['first_name']
    last_name = form_data['last_name']
    image_url = form_data['image_url'] or None

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )
    # flash message for successful addition
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get("/users/<int:id>")
def render_user_profile(id):
    ''' Renders user profile '''
    current_user = User.query.get_or_404(id)
    posts = current_user.posts

    return render_template(
        "user_profile.html",
        current_user=current_user,
        posts=posts)


@app.get("/users/<int:id>/edit")
def show_form(id):
    ''' Renders form for editing user'''
    current_user = User.query.get_or_404(id)

    return render_template("edit_user.html", current_user=current_user)


@app.post('/users/<int:id>/edit')
def edit_user(id):
    ''' Edits user profile '''
    current_user = User.query.get_or_404(id)

    current_user.first_name = request.form['first_name']
    current_user.last_name = request.form['last_name']

    if not request.form['image_url']:
        # This is the edit area where None is not required
        current_user.image_url = DEFAULT_IMAGE_URL
    else:
        current_user.image_url = request.form['image_url']

    db.session.commit()
    return redirect(f'/users/{id}')


@app.post("/users/<int:id>/delete")
def delete_user(id):
    ''' Deletes user '''
    current_user = User.query.get_or_404(id)
    # TODO: why doesn't current_user.posts.clear() work here? use .delete()
    Post.query.filter(Post.user_id == id).delete()

    db.session.delete(current_user)

    db.session.commit()

    flash(
        f"User: {current_user.first_name} {current_user.last_name} has been deleted successfully")

    return redirect("/")


@app.get("/posts/<int:id>")
def view_post(id):
    ''' View a post '''
    current_post = Post.query.get_or_404(id)

    return render_template('post_detail.html', current_post=current_post)


@app.get("/users/<int:id>/posts/new")
def render_new_post_form(id):
    ''' Renders form for new post '''
    current_user = User.query.get_or_404(id)

    return render_template("new_post_form.html", current_user=current_user)

#TODO: look for a user first
@app.post("/users/<int:id>/posts/new")
def handle_new_post(id):
    ''' Adds new post'''
    form_data = request.form
    title = form_data["title"]
    content = form_data["content"]

    new_post = Post(
        title=title,
        content=content,
        user_id=id
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{id}")


@app.get("/posts/<int:id>/edit")
def render_edit_post_form(id):
    ''' Renders form to edit post '''
    current_post = Post.query.get_or_404(id)

    return render_template("edit_post.html", current_post=current_post)


@app.post("/posts/<int:id>/edit")
def edit_post(id):
    ''' Handle form submission to edit existing post '''
    current_post = Post.query.get_or_404(id)

    current_post.title = request.form['title']
    current_post.content = request.form['content']
    current_post.created_at = db.func.now()
    #we would want another column instead since it's an edit

    db.session.commit()
    return redirect(f'/posts/{id}')


@app.post('/posts/<int:id>/delete')
def delete_post(id):
    ''' Deletes post from posts and redirects to current user '''
    current_post = Post.query.get_or_404(id)

    db.session.delete(current_post)
    db.session.commit()

    flash(f"{current_post.title} has been deleted successfully")

    return redirect(f"/users/{current_post.user_id}")
