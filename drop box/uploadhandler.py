import webapp2
import jinja2
# google related imports
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import blobstore_handlers
from myuser import MyUser
from directory import directory
# class to take care of upload operation
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        presentfolder = self.request.get('presentfolder')
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        file = blobinfo.filename
        flag = 0

        dir_key = ndb.Key('directory', presentfolder)
        dir = dir_key.get()
        if not dir:
            dir = directory(id = presentfolder)
        dir.file = file
        dir.directoryName = presentfolder
        dir.fileBool = True
        dir.blobname = upload.key()

        my_user_key = ndb.Key('MyUser', user.user_id())
        my_user = my_user_key.get()
        if my_user == None:
            my_user = MyUser(id = user.user_id())
        my_user.username = user.user_id()

        for x in my_user.directory:
            if x.file == file:
                flag = 1

        if  flag == 0:
            my_user.directory.append(dir)
            my_user.put()

        self.redirect('/')
