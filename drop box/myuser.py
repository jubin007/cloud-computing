from google.appengine.ext import ndb
from directory import directory
# Object responsible for User
class MyUser(ndb.Model):
    username = ndb.StringProperty()
    # object responsible for Directory or Folder
    directory = ndb.StructuredProperty(directory, repeated=True)
