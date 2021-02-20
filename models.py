from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)
    
    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False, default="https://t4.ftcdn.net/jpg/03/46/93/61/360_F_346936114_RaxE6OQogebgAWTalE1myseY1Hbb5qPM.jpg")

    Post = db.relationship('Post', backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    __tablename__ = "Posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable = False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'),  nullable=False)
    
    # user = db.relationship('User', backref="Post",)
  

class PostTag(db.Model):
    __tablename__ = "Posttag"

    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'), nullable=False, primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('Tag.id'), nullable=False, primary_key=True)

    

class Tag(db.Model):
    __tablename__ = "Tag"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    name = db.Column(db.Text, unique = True)

    posts = db.relationship('Post', secondary="Posttag", backref="tags")
