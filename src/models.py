import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    bio = Column(String(250))
    profile_picture = Column(String)
    website = Column(String)
    posts = relationship("Post", back_populates="user")
    followers = relationship("Followers", primaryjoin="User.id==Followers.user_id", back_populates="user")
    following = relationship("Following", primaryjoin="User.id==Following.user_id", back_populates="user")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(String, nullable=False)
    caption = Column(String(250))
    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post")
    created_at = Column(DateTime)

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    created_at = Column(DateTime)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    content = Column(String(250), nullable=False)
    created_at = Column(DateTime)

class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="followers", foreign_keys=[user_id])
    follower = relationship("User", back_populates="following", foreign_keys=[follower_id])

class Following(Base):
    __tablename__ = 'following'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="following", foreign_keys=[user_id])
    following_user = relationship("User", back_populates="followers", foreign_keys=[following_id])

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
