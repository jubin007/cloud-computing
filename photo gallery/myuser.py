from google.appengine.ext import ndb

class MyUser(ndb.Model):
    galleries = ndb.StringProperty(repeated = True)
