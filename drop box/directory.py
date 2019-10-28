from google.appengine.ext import ndb
# Object for Folder/directory related data like name, file
class directory(ndb.Model):
    directoryName = ndb.StringProperty()
    file = ndb.StringProperty()
    fileBool = ndb.BooleanProperty()
    blobname = ndb.BlobKeyProperty()
