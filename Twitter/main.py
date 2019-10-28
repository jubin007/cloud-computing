import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from myuser import MyUser
from definitions import Definitions
from editpage import EditPage
from tweet import Tweet
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):

        self.response.headers["Content-Type"] = "text/html"
        user = Definitions().get_current_user()
        myuser = None
        tweets = None
        edit_tweet = None

        if user:

            url = users.create_logout_url(self.request.uri)
            myuser_key = ndb.Key("MyUser", Definitions().get_current_user_id())
            myuser = myuser_key.get()
            user_name = self.request.GET.get("user_name")
            bio = self.request.GET.get("bio")


            if myuser == None:
                myuser = Definitions().create_user(user_id= user.user_id(), email_address=user.email())



            if user_name != None and user_name != "" and bio != None and bio != "":

                user_query = MyUser.query(MyUser.user_name == user_name).fetch()

                if len(user_query) > 0:
                    self.redirect("/")
                    return

                myuser.user_name = user_name
                myuser.bio = bio
                myuser.put()

            tweets = Tweet.query().order(-Tweet.time)
            search = self.request.GET.get("query")

            if search == "user" or search == "post":

                search_text = self.request.GET.get("search_text")

                if len(search_text) > 0:

                    if search == "user":
                        tweets = Definitions().search_by_user(text=search_text)
                    else:
                        tweets = Definitions().search_by_tweet(text=search_text)


            elif search == "Delete" or search == "Edit":

                query = self.request.GET.get("query")
                tweet_id = self.request.GET.get("tweet_id")

                if query == "Edit":
                    edit_tweet = Definitions().get_tweet(tweet_id = tweet_id)
                else:
                    Definitions().delete_tweet(tweet_id = tweet_id)

            else:
                tweets = []
                for tweet in Tweet.query().order(-Tweet.time).fetch():
                    if tweet.user_id in myuser.following or tweet.user_id == myuser.key.id():
                        tweets.append(tweet)

        else:
            url = users.create_login_url(self.request.uri)


        template_values = {
            "url": url,
            "myuser": myuser,
            "edit_tweet":edit_tweet,
            "tweets":tweets,
            "upload_url" : blobstore.create_upload_url('/upload_photo')
        }

        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers["Content-Type"] = "text/html"

        text_share = self.request.get("text_share")
        share_image = self.request.get("share_image")


        if text_share != None or text_share != "":

            share_type = self.request.get("share_type")

            if share_type == "Update":

                edit_tweet_id = self.request.get("edit_tweet_id")
                edit_tweet = Definitions().get_tweet(tweet_id=edit_tweet_id)
                edit_tweet.text_share = text_share

                edit_tweet.put()

            else:

                myuser = Definitions().get_login_user()
                tweet = Tweet(text_share = text_share,
                              user_id = myuser.key.id(),
                              user_name = myuser.user_name,
                               time = datetime.datetime.now())
                tweet.put()

                myuser.tweets_id.append(tweet.key.id())
                myuser.put()

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


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ("/editpage", EditPage),
], debug=True)
