import secrets
from xmlrpc.client import Boolean
from PIL import Image
import os
from webapp.models import User, Event
from webapp import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, request, abort
from webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, EventForm, SearchFriendForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')


@app.route("/home")
@login_required
def home():
    searchform = SearchFriendForm()
    user_events = Event.query.filter_by(owner=current_user.username)
    
    rsvp_events = current_user.rsvp
    if searchform.validate_on_submit():
        searcheduser = User.query.filter_by(username = searchform.user.data)
        if searcheduser:
            return redirect(url_for('view_user', user_id = searcheduser.id))
    return render_template('home.html', events=user_events, rsvp_events=rsvp_events)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('home'))  # USE THE NAME OF THE FUNCTION NOT THE NAME OF THE HTML FILE, redirecting to homepage after register
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # Checking if the inputted password matches the actual password
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # Redirects you to next page if you tried to access the page and were redirected to the login
            return redirect(next_page) if next_page else redirect(url_for('home')) # check if next_page is safe
        else: 
            flash('Login Unsuccessful. Incorrect Email or Password', 'danger') # Shows failed login message using bootstrap class 'danger'
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))


def save_picture(form_picture): # Creates a path to the picture that the user uploaded
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # Splitting the image into the name and it's extension, used '_' as a throwaway variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form=form)



@app.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        event = Event(title=form.title.data, time=form.time.data, detail=form.detail.data, owner=current_user.username, date=form.date.data)
        db.session.add(event)
        db.session.commit()
        participants = form.rsvps.data
        
        particp_list = participants.split(", ")

        for particip in particp_list:
            user = User.query.filter_by(username=particip).first()
            event.rsvps.append(user)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('create_event.html', title='New Post', form=form, legend='New Event')



@app.route("/user/<int:user_id>")
def view_user(user_id):
    return render_template('other_user.html', user=user_id)

@app.route("/event/<int:event_id>")
def view_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    return render_template('view_event.html', event=event)

