"""predictions of users based on tweet embeddings"""
import numpy as np 
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet
from .models import User


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and return which user is more likely to say a hypothetical tweet.

    example run: predicts_user("elonmusk", "jackblakc", 
                               "school of rock really rocks")
    returns 0 (user0_name=elonmusk) or 1 (user1name=jackblack)
    """

    # grab users from database
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # grabbing vectors from each tweet in user.tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # vertically stack (combine vectors) to train model
    vects = np.vstack([user0_vects, user1_vects])

    # generate labels for vects array
    labels = np.concatenate([np.zeros(len(user0.tweets)),
                             np.ones(len(user1.tweets))])

    # instantiate and train model
    log_reg = LogisticRegression().fit(vects, labels)

    # use nlp to generate embeddings - vectorize tweet()
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)

    # predicts and returns 0 or 1 depending upone logistic regression models prediction
    return log_reg.predict(hypo_tweet_vect)


