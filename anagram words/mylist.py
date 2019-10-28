from google.appengine.ext import ndb
from mynumb import MyNumb

class MyList(ndb.Model):
    anagrams = ndb.StringProperty(repeated=True)
    no_words = ndb.IntegerProperty(default=0)
    no_letters = ndb.IntegerProperty(default=0)
