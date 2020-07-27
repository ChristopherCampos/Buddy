"""
The database models used for storing Users and Posts
"""
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

DATABASE_NAME = "buddy_db"
database_path = "postgres://{}/{}".format('localhost:5432', DATABASE_NAME)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """Simply sets up db with specific database and configuration"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db


class User(db.Model):
    """Models a user table in a relational database"""
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True, nullable=False)
    post_count = Column(Integer)
    friend_count = Column(Integer)
    posts = db.relationship('Post', backref="user", lazy=True)

    def __repr__(self):
        return "<{0}>: {1}".format(self.user_id, self.username)

    def __init__(self, username):
        self.username = username

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Post(db.Model):
    """Models a post that a user can post to their account."""
    __tablename__ = "Post"
    post_id = Column(Integer, primary_key=True)
    content = Column(String(150), nullable=False)
    user_id = Column(Integer, db.ForeignKey('User.user_id'), nullable=False)

    def __repr__(self):
        return "<{0}>: {1}".format(self.post_id, self.user_id)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


