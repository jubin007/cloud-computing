from google.appengine.ext import ndb
class MyUser(ndb.Model):
	email_address = ndb.StringProperty()
	name = ndb.StringProperty(repeated = True)
