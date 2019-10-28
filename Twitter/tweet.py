from google.appengine.ext import ndb

class Tweet(ndb.Model):
    user_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    text_share = ndb.StringProperty()
    time = ndb.DateTimeProperty()
    Blob = ndb.BlobProperty()
