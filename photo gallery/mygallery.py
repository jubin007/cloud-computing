from google.appengine.ext import ndb
from myimage import MyImage

class MyGallery(ndb.Model):
    images = ndb.StructuredProperty(MyImage, repeated = True)
