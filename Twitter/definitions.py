from google.appengine.api import users
from google.appengine.ext import ndb

from itertools import permutations
from tweet import Tweet
from myuser import MyUser

class Definitions(object):

    def create_user(self,user_id,email_address):

        myuser = MyUser(id=user_id, user_id=str(user_id), email_address=str(email_address))
        myuser.user_name = ""
        myuser.following = []
        myuser.put()
        return myuser

    def get_current_user(self):
        return users.get_current_user()


    def get_current_user_id(self):
        return users.get_current_user().user_id()




    def get_login_user(self):
        myuser_key = ndb.Key("MyUser", Definitions().get_current_user_id())
        return  myuser_key.get()

    def search_by_tweet(self,text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return Tweet.query(Tweet.text_share >= text, Tweet.text_share < limit)

    def search_by_user(self,text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return Tweet.query(Tweet.user_name >= text, Tweet.user_name < limit)

    def delete_tweet(self,tweet_id):

        myuser = Definitions().get_login_user()
        tweets_id = myuser.tweets_id
        tweets_id.remove(int(tweet_id))
        myuser.tweets_id = tweets_id
        myuser.put()

        tweet_key = ndb.Key("Tweet", int(tweet_id))
        tweet = tweet_key.get()
        tweet.key.delete()


    def get_tweet(self,tweet_id):

        tweet_key = ndb.Key("Tweet", int(tweet_id))
        tweet = tweet_key.get()
        return tweet
