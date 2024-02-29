"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request, flash, session
from models import connect_db, User, db, DEFAULT_IMAGE_URL

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


@app.post('/users')
def add_user():
    ''' Adds user and redirects to users page '''
    form_data = request.form
    first_name = form_data['first_name']
    last_name = form_data['last_name']
    # This handles the falsy value in the if statement in edit below
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

    return render_template("user_profile.html", current_user=current_user)


@app.get("/users/<int:id>/edit")
def show_form(id):
    # be more specific on this docstring, conflicts with above
    ''' Shows user profile '''
    current_user = User.query.get_or_404(id)

    return render_template("edit_user.html", current_user=current_user)


@app.post('/users/<int:id>/edit')
def edit_user(id):
    ''' Edits user profile '''
    current_user = User.query.get_or_404(id)

    current_user.first_name = request.form['first_name']
    current_user.last_name = request.form['last_name']
    if(request.form['image_url'] == ""):
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

    db.session.delete(current_user)

    db.session.commit()

    flash(f"User: {current_user.first_name} {current_user.last_name} \
          has been deleted successfully")

    return redirect("/")
