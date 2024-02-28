"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from models import connect_db, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def users_redirect():
    return redirect("/users")

@app.get("/users")
def render_user_page():
    users = User.query.all()

    return render_template("users_list.html", users=users)

@app.get("/users/new")
def render_new_user_form():
    return render_template("new_user_form.html")

@app.post('/users')
def add_user():
    form_data = request.form
    first_name = form_data['first_name']
    last_name = form_data['last_name']
    image_url = form_data['image_url']

    new_user = User(
        first_name = first_name,
        last_name = last_name,
        image_url = image_url
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get("/users/<int:id>")
def render_user_profile(id):
    current_user = User.query.get_or_404(id)

    first_name = current_user.first_name
    last_name = current_user.last_name
    image_url = current_user.image_url

    return render_template("user_profile.html", first_name=first_name, last_name=last_name, image_url=image_url, id=id)

