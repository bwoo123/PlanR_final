from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '4cfa18ca495de03e65dd0a937cc035d2'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)    # SQL database
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'  # Sends the user to the login screen if @login.required is found on any of the routes (i.e accessing one's account)
# login_manager.login_message_category = 'info' # gives bootstrap class 'info' to login message

from webapp import routes