"""retreive Tweets, embeddings, and push to database"""
from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User


# Connect to twitter API with twitter api key and secret key

TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_API_KEY'),
                                   getenv('TWITTER_API_SECRET_KEY'))
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load("my model")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        """Adds user with username 'username' to our database"""
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # TODO - fix assumption on continuously new tweets
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode="extended")

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[0:300],
                             vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        DB.session.commit()