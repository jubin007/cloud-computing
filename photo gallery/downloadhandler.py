import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):

    def get(self):

        user = users.get_current_user()
        if not user:
            return self.redirect('/error')

        my_name = self.request.get('name').strip()
        if not my_name:
            return self.redirect('/error')

        my_image = self.request.get('image').strip()
        if not my_image:
            return self.redirect('/error')

        my_gallery_key = ndb.Key('MyGallery', user.user_id() + "-" + my_name)
        my_gallery = my_gallery_key.get()
        if not my_gallery:
            return self.redirect('/error')

        for image in my_gallery.images:
            if my_image == image.name:
                return self.send_blob(image.blob)
