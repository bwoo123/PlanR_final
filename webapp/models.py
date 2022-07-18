from webapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# RSVPs = db.Table('RSVPs',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
#     db.Column('going', db.Boolean, nullable=False, default=False)
# )

class RSVP(db.Model):
    __tablename__ = "RSVP"
    event_rsvp_id = db.Column(db.ForeignKey("event.id"), primary_key=True)
    user_rsvp_id = db.Column(db.ForeignKey("user.id"), primary_key=True)
    
    going = db.Column(db.String(1), default='n')

    user = db.relationship("User", backref="user_rsvps")
    event = db.relationship("Event", backref="event_rsvps")

    def __repr__(self):
        return f"RSVP('{self.event_rsvp_id}', '{self.user_rsvp_id}', '{self.going}')"

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    friends = db.relationship('Friendship', backref='friend', lazy=True)

    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    time = db.Column(db.String)
    detail=db.Column(db.Text)
    owner=db.Column(db.Integer)
    date=db.Column(db.String)

    rsvps = db.relationship('User', secondary="RSVP", backref='rsvp')

    def __repr__(self):
        return f"Event('{self.title}', '{self.time}')"

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    friend_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"User('{self.friend_id}', '{self.user_id}')"