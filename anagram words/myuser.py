from google.appengine.ext import ndb

class MyUser(ndb.Model):
	email_address = ndb.StringProperty()
	lists = ndb.StringProperty(repeated = True)
