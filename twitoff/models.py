"""SQLAlchemy models and utility functions for Twitoff"""
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB = SQLAlchemy()
MIGRATE = Migrate()

# User Table
class User(DB.Model):
    """Twitter users correspoding to tweets"""
    # primary ID column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # name column
    name = DB.Column(DB.String, nullable=False)
    # keeps track of users most recent tweet
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)


# """CREATE TABLE User (id PRIMARY AUTOINCREMENT, name VARCAR(30))""""

# tweet table
class Tweet(DB.Model):
    """Tweet text and data"""
    # primary id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column of character length 300(unicode)
    text = DB.Column(DB.Unicode(300))
    # vectorized tweet column, pickled (hehe)
    vect = DB.Column(DB.PickleType, nullable=False)
    # foreign key - user.id
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'),
                        nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


def insert_example_user():
    """Will get error if ran twice since data already existsa"""
    bobby = User(id=1, name="bobbybri")
    aoc = User(id=2, name="AOC")
    DB.session.add(bobby)  # adds bobby user
    DB.session.add(aoc)  # adds aoc user
    DB.session.commit()


def insert_example_tweet(count=6):
    """Will get error if ran twice since data already existsa"""
    tweets = []

    tweet_text = ["I like pie", "lets play some dota",
                  "woshoigomaewoacanchinkochazhinschischi", "I ate good soup",
                  "I like toaster strudel", "meepmeep"]
    while count > 0:
        id = count
        text = random.choice(tweet_text)
        user_id = random.randint(1, 2)

        tweet = Tweet(id=id, text=text, user_id=user_id)
        tweets.append(tweet)
        count -= 1

    DB.session.add_all(tweets)

    DB.session.commit()
