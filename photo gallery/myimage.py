from google.appengine.ext import ndb

class MyImage(ndb.Model):
    name = ndb.StringProperty()
    blob = ndb.BlobKeyProperty()
