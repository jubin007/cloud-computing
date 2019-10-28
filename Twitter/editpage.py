import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from definitions import Definitions
from tweet import Tweet
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class EditPage(webapp2.RedirectHandler):

    def get(self):

        self.response.headers["Content-Type"] = "text/html"
        user_id = self.request.GET.get("user_id")
        spectator = True
        follow = "Follow"

        if user_id != None:
            myuser_key = ndb.Key("MyUser", user_id)
            myuser = myuser_key.get()

            tweets = Tweet.query(Tweet.user_id == myuser.key.id()).fetch(50)
            if user_id == str(Definitions().get_login_user().key.id()):
                spectator = False
            if user_id in Definitions().get_login_user().following:
                follow = "Unfollow"

        template_values = {
            "myuser": myuser,
            "follow":follow,
            "tweets":tweets,
            "spectator":spectator,
        }

        template = JINJA_ENVIRONMENT.get_template("editpage.html")
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        user_id = self.request.get("user_id")

        if self.request.get("update") == "Update":

            # if self.request.get("date") =="" or user_id == "":
            #     self.redirect("/editpage")
            #     return

            myuser = Definitions().get_login_user()
            user_first_name = self.request.get("user_first_name")
            user_last_name = self.request.get("user_last_name")
            myuser.first_name = user_first_name
            myuser.last_name = user_last_name
            myuser.put()
            self.redirect("/")

        elif self.request.get("followusers") == "Follow" or self.request.get("followusers") == "Unfollow":

            myuser = Definitions().get_login_user()

            if self.request.get("followusers") == "Follow":
                myuser.following.append(user_id)

            else:
                following = myuser.following
                following.remove(user_id)
                myuser.following = following

            myuser.put()
            self.redirect("/editpage?user_id={}".format(user_id))

        if self.request.get("cancel"):
            self.redirect("/")

class Edit(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()

		my_name = self.request.get('name').strip()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()
		my_list_key = ndb.Key('MyList', user.user_id() + "-" + my_name)
		my_list = my_list_key.get()
		my_gpu_key = ndb.Key('GPU', user.user_id())
		my_gpu = my_gpu_key.get()


		template_values = {
			'my_name' : my_name,
			'my_list': my_list,
			'myuser' : myuser,
			'my_gpu' : my_gpu
		}
		template = JINJA_ENVIRONMENT.get_template('edit.html')
		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()
		my_name = self.request.get('name').strip()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()


		if self.request.get('button') == 'Update':
			my_list = MyList(id = user.user_id() + "-" + my_name)
			my_list.ManufacturerName = self.request.get('users_GPU')
			DateIssued = self.request.get('users_DateIssued')
			new_date = datetime.strptime(DateIssued, '%Y-%m-%d')
			my_list.DateIssued = new_date
			my_list.GeometryShader = bool(self.request.get('users_GeometryShader'))
			my_list.TesselationShader = bool(self.request.get('users_TesselationShader'))
			my_list.ShaderInt16 = bool(self.request.get('users_ShaderInt16'))
			my_list.SparseBinding = bool(self.request.get('users_SparseBinding'))
			my_list.TextureCompressionETC2 = bool(self.request.get('users_TextureCompressionETC2'))
		 	my_list.VertexPipelineStoresAndAtomics = bool(self.request.get('users_VertexPipelineStoresAndAtomics'))
			new_gpu = GPU(ManufacturerName=my_list.ManufacturerName,DateIssued=my_list.DateIssued,GeometryShader=my_list.GeometryShader,TesselationShader=my_list.TesselationShader,ShaderInt16=my_list.ShaderInt16,SparseBinding=my_list.SparseBinding,TextureCompressionETC2=my_list.TextureCompressionETC2,VertexPipelineStoresAndAtomics=my_list.VertexPipelineStoresAndAtomics)
			my_list.gpuset.append(new_gpu)
			my_list.put()
			self.redirect('/')

		elif self.request.get('button')	== 'Cancel':
			 self.redirect('/')
