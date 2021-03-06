import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql.schema import ForeignKey

# user = 'jorgecruz'
# database_name = "moviecenter"
# database_path = "postgres://{}@{}/{}".format(
#     user, 'localhost:5432', database_name)

database_path = "postgres://rltmaysaktlhfi:bb1364d8983783f48581cc1dad589b587cc437b50d12eb196204f27a55dacbc1@ec2-54-211-210-149.compute-1.amazonaws.com:5432/df67o3decn2789"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    released = Column(DateTime, nullable=False)
    picture_link = Column(String)
    synopsis = Column(String)
    cast = relationship("Cast", backref="movies",
                        cascade="all,delete,delete-orphan")

    def __init__(self, title, released, picture_link, synopsis):
        self.title = title
        self.released = released
        self.picture_link = picture_link
        self.synopsis = synopsis

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'released': self.released,
            'picture_link': self.picture_link,
            'synopsis':self.synopsis
        }


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    picture_link = Column(String)
    bio = Column(String)
    cast = relationship("Cast", backref="actors",
                        cascade="all,delete,delete-orphan")

    def __init__(self, name, age, gender, picture_link, bio):
        self.name = name
        self.age = age
        self.gender = gender
        self.picture_link = picture_link
        self.bio = bio

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'picture_link': self.picture_link,
            'bio':self.bio
        }


class Cast(db.Model):
    __tablename__ = "casts"
    id = Column(Integer, primary_key=True)
    actors_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
    movies_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
