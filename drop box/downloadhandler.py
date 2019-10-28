import webapp2
import jinja2
# Google related imports
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from myuser import MyUser
from directory import directory
# class for download/delete operation
class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        user = users.get_current_user()
        presentfolder = self.request.get('presentfolder')
        index = int(self.request.get('index'))
        file = self.request.get('file')
        action = self.request.get('Download')
        # download file
        if action == 'Download':
            my_user_key = ndb.Key('MyUser', user.user_id())
            my_user = my_user_key.get()
            if my_user:
                for d in xrange(len(my_user.directory)):
                    if my_user.directory[d].directoryName == presentfolder:
                        if my_user.directory[d].file == file:
                            self.send_blob(my_user.directory[d].blobname)
        # delete operation
        elif action == 'Delete':
            my_user_key = ndb.Key('MyUser', user.user_id())
            my_user = my_user_key.get()
            if my_user:
                for d in xrange(len(my_user.directory)):
                    if my_user.directory[d].directoryName == presentfolder:
                        if my_user.directory[d].file == file:
                            del my_user.directory[d].blobname
                            my_user.put()
            self.redirect('/')
