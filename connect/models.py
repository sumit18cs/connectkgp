from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from connect import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))
 


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(50), unique=False, default='Not Given')
    rollno = db.Column(db.String(20), unique=False, default='Not Given')
    hall = db.Column(db.String(100), unique=False, default='None')
    department = db.Column(db.String(100), unique=False, default='None')
    support=db.Column(db.String(20),unique=False,default='Yes')

    doubts = db.relationship('Doubt', backref='author', lazy=True)
    jobs = db.relationship('Job', backref='author', lazy=True)
    collabs = db.relationship('Collab', backref='author', lazy=True)
    skills = db.relationship('Skill', backref='author', lazy=True)

    messages_sent = db.relationship('Chat',foreign_keys='Chat.sender_id',backref='author', lazy='dynamic')
    messages_received = db.relationship('Chat',foreign_keys='Chat.recipient_id',backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Chat.query.filter_by(recipient=self).filter(Chat.timestamp > last_read_time).count()




    def __repr__(self):
        return "User('{self.username}', '{self.email}', '{self.image_file}')"


    followed = db.relationship('User', secondary=followers,primaryjoin=(followers.c.follower_id == id),secondaryjoin=(followers.c.followed_id == id),backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0


    


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

 
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)#utc

    def __repr__(self):
        return "Chat('{self.body}','{self.timestamp}')"  



class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False,default='None')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Skill('{self.title}', '{self.date_posted}')"


class Doubt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='author', lazy=True)
    def __repr__(self):
        return "Doubt('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(1000), nullable=False)
    doubt_id = db.Column(db.Integer, db.ForeignKey('doubt.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Comment('{self.message}', '{self.date_posted}')"



class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    jobcomments = db.relationship('Jobcomment', backref='author', lazy=True)
    def __repr__(self):
        return "Job('{self.title}', '{self.date_posted}')"

class Jobcomment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(1000), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Jobcomment('{self.message}', '{self.date_posted}')"



class Collab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collabcomments = db.relationship('Collabcomment', backref='author', lazy=True)
    def __repr__(self):
        return "Collab('{self.title}', '{self.date_posted}')"

class Collabcomment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(1000), nullable=False)
    collab_id = db.Column(db.Integer, db.ForeignKey('collab.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Collabcomment('{self.message}', '{self.date_posted}')"
