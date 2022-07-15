import secrets
from PIL import Image
import os
#from webapp.models import User, Post
from webapp import app#, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
#from webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required

EVENTS = [
    {
        'event': "Bob's Birthday",
        'people': ["Bob", "James", "Ashley"],
        'location': "White Spot",
        'date': "Jan. 1st 2022",
        'time': "7:00pm",
        'id': 1
    },

    {
        'event': "Thor Movie",
        'people': ["Jim", "James", "Ashley"],
        'location': "Marine Gateway",
        'date': "Jan. 2nd, 2022",
        'time': "9:00pm",
        'id': 2
    },

    {
        'event': "Dinner",
        'people': ["Jim", "James", "Ashley"],
        'location': "Red Robin",
        'date': "Jan. 3rd, 2022",
        'time': "6:00pm",
        'id': 3
    }
]


@app.route("/")
@app.route("/welcome")
def welcome():
    #posts = Post.query.all()
    return render_template('welcome.html')


@app.route("/home")
def home():
    return render_template('home.html', events=EVENTS)

@app.route("/register")
def register():
    return render_template('register.html')