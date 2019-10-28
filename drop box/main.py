import webapp2
import jinja2
import os
# imports from Google
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import users
# local imports
from uploadhandler import UploadHandler
from downloadhandler import DownloadHandler
from myuser import MyUser
from directory import directory
# Framework configuration
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        # list of folders
        folders = []
        #current directory
        presentfolder = ''
        #object for Toggler
        action = self.request.get('toggle')
        redirect = self.request.get('redirect')
        x = 0
        url = ""
        flag = 0
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            template_values = {'url' : users.create_login_url(self.request.uri)  }
            template = JINJA_ENVIRONMENT.get_template('guestpage.html')
            self.response.write(template.render(template_values))
            return

        url = users.create_logout_url(self.request.uri)

        my_user_key = ndb.Key('MyUser', user.user_id())
        my_user = my_user_key.get()

        if my_user == None:
            my_user = MyUser(id = user.user_id())
            dir = directory()
            dir.directoryName = '/'
            dir.file = ""
            dir.fileBool = False
            dir.blobname = None
            my_user.directory.append(dir)
            my_user.put()

        for x in xrange(len(my_user.directory)):
            flag = 0
            for i in folders:
                if i == my_user.directory[x].directoryName:
                    flag = 1
            if flag == 0 and my_user.directory[x].directoryName != None:
                folders.append(my_user.directory[x].directoryName)

        for x in xrange(len(my_user.directory)):
            if my_user.directory[x].directoryName != None:
                presentfolder = my_user.directory[x].directoryName
                if (my_user.directory[x].directoryName == redirect):
                    break

        if action == 'Toggler':
            #go up one level
            cd = self.request.get('my_index')
            lastdir = ''
            for x in xrange(len(my_user.directory)):
                if my_user.directory[x].directoryName != None:
                    if (my_user.directory[x].directoryName == cd):
                        break
                    lastdir = my_user.directory[x].directoryName
            self.redirect('/?redirect='+lastdir)

        #Picks the uploaded files by the current user
        myuser = MyUser.query()
        myuser = myuser.filter(MyUser.username == user.user_id())
        myuser = myuser.filter(MyUser.directory.directoryName == presentfolder)
        myuser = myuser.fetch()

        template_values = {
            'url' : url,
            'user' : user,
            'myuser' : myuser,
            'presentfolder' : presentfolder,
            'folders' : folders,
            'upload_url' : blobstore.create_upload_url('/upload?dir=')
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        flag2 = 0
        action = self.request.get('folderOperation')
        user = users.get_current_user()
        my_user_key = ndb.Key('MyUser', user.user_id())
        my_user = my_user_key.get()
        if my_user == None:
            my_user = MyUser(id = user.user_id())

        #To create new folder
        if action == 'Create Folder':
            directoryName = self.request.get('directoryName')

            my_user.username = user.user_id()
            for my_dir in xrange(len(my_user.directory)):
                if my_user.directory[my_dir].directoryName == directoryName:
                    flag2 = 1

            if flag2 == 0:
                dir = directory(id = directoryName, file='', directoryName=directoryName, fileBool=False, blobname=None)
                my_user.directory.append(dir)
                my_user.put()

        # To delete folder
        elif action == 'Delete Folder':
            my_user_key = ndb.Key('MyUser', user.user_id())
            my_user = my_user_key.get()
            if my_user == None:
                my_user = MyUser(id = user.user_id())
            deletionFolder = self.request.get('deletionFolder')

            for d in xrange(len(my_user.directory)):
                if my_user.directory[d].directoryName == deletionFolder:
                    if deletionFolder != '/':
                        del my_user.directory[d].directoryName
                        my_user.put()
                        self.redirect('/')

        self.redirect('/')

app = webapp2.WSGIApplication([('/', MainPage),('/upload', UploadHandler),('/download', DownloadHandler)])
