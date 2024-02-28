"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from models import connect_db, User

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