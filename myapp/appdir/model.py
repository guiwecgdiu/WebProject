from appdir import db
from datetime import datetime

class User(db.Model):
    """docstring for ."""
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128),unique=True)
    posts=db.relationship('Post',backref='user')

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    """docstring for ."""
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(140))
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post{} >'.format(self.body)
