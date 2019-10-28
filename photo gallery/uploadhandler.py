from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from mygallery import MyGallery
from myimage import MyImage

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        user = users.get_current_user()
        if not user:
            return self.redirect('/error')

        my_name = self.request.get('name').strip()
        if not my_name:
            return self.redirect('/error')

        my_gallery_key = ndb.Key('MyGallery', user.user_id() + "-" + my_name)
        my_gallery = my_gallery_key.get()
        if not my_gallery:
            return self.redirect('/error')

        for upload in self.get_uploads():

            blobinfo = blobstore.BlobInfo(upload.key())
            filename = blobinfo.filename.lower()

            if not filename.endswith(".jpg"):
                return self.redirect('/error')

            for image in my_gallery.images:
                if filename == image.name:
                    return self.redirect('/error')

            my_image = MyImage()
            my_image.name = filename
            my_image.blob = upload.key()

            my_gallery.images.append(my_image)

        my_gallery.put()

        self.redirect('/gallery?name=' + my_name)
