import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from mylist import MyList
from mynumb import MyNumb
import os

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['content-type'] = 'text/html'

		myword = ''
		search_string = ''
		myanagrams = []
		url = ''
		url_string = ''
		myuser = None
		words = []
		welcome = 'Welcome back'

		user = users.get_current_user()

		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'

			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()

			if myuser is None:
				welcome = 'Welcome to the application'
				myuser = MyUser(id=user.user_id())
				myuser.put()
			words.append(len(myuser.lists))

			if self.request.get('search'):
				search_string = self.request.get('name')
				sorted_search_string = list(search_string)
				sorted_search_string.sort()
				for item in myuser.lists:
					list_str1 = list(item)
					list_str1.sort()
					if list_str1 == sorted_search_string:
						mykey = ndb.Key('MyList', user.user_id() + "-" + item)
						mykey = mykey.get()
						myword = item
						myanagrams = mykey.anagrams

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

	 	template_values = {
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'myuser' : myuser,
			'words': words,
			'myword' : myword,
			'myanagrams' : myanagrams,
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

	def post(self):


		self.redirect("/")


class DictPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['content-type'] = 'text/html'

		url = ''
		url_string = ''
		myuser = None
		no_words = []
		welcome = 'Welcome back'

		user = users.get_current_user()

		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'

			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()

			if myuser is None:
				welcome = 'Welcome to the application'
				myuser = MyUser(id=user.user_id())
				myuser.put()

			for list in myuser.lists:
				my_list_key = ndb.Key('MyList', user.user_id() + "-" + list)
				my_list = my_list_key.get()
				no_words.append(len(my_list.anagrams))
		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

	 	template_values = {
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'myuser' : myuser,
			'no_words': no_words,
		}

		template = JINJA_ENVIRONMENT.get_template('dictionary.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		my_name = self.request.get('name').strip()
		new_letter = self.request.get('no_letters').strip()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()

		if self.request.get('add'):

			isAddedToAnagrams = False
			if not my_name in myuser.lists:
				for item in myuser.lists:
					list_str1 = list(item)
					list_str2 = list(my_name)
					list_str1.sort()
					list_str2.sort()
					if list_str1 == list_str2:
						isAddedToAnagrams = True
						#check all its already added anagrams
						mylist = ndb.Key('MyList', user.user_id() + "-" + item)
						mylist = mylist.get()
						if my_name not in mylist.anagrams:
							#add this to anagram list
							mylist.anagrams.append(my_name)
							mylist.no_words = len(mylist.anagrams)
							mylist.put()

				if(isAddedToAnagrams == False):
					my_new_list = MyList(id = user.user_id() + "-" + my_name)
					myuser.lists.append(my_name)
					my_new_list.no_letters = len(my_name)
					my_new_list.put()
					myuser.put()

		elif self.request.get('delete'):
			my_list_key = ndb.Key('MyList', user.user_id() + "-" + my_name)
			my_list = my_list_key.get()

			my_list_key.delete()

			myuser.lists.remove(my_name)
			myuser.put()

		self.redirect("/dictionary")

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/dictionary', DictPage)
], debug=True)
