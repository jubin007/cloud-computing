from google.appengine.ext import ndb
from tweet import Tweet

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    user_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    bio = ndb.StringProperty()
    tweets_id = ndb.IntegerProperty(repeated=True)
    following = ndb.StringProperty(repeated=True)
    follower = ndb.StringProperty(repeated=True)
