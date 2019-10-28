import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from mygallery import MyGallery
from google.appengine.ext import blobstore
from uploadhandler import UploadHandler
from downloadhandler import DownloadHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class ErrorPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-type'] = 'text/html'
        self.response.write("an error occurred. <a href='/'>go to main page</a>")

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-type'] = 'text/html'

        url = ''
        url_string = ''
        my_user = None
        my_sizes = []

        user = users.get_current_user()

        if user:
            url = users.create_logout_url("/")
            url_string = 'logout'

            my_user_key = ndb.Key('MyUser', user.user_id())
            my_user = my_user_key.get()
            if my_user is None:
                my_user = MyUser(id = user.user_id())
                my_user.put()

            for gallery in my_user.galleries:
                my_gallery_key = ndb.Key('MyGallery', user.user_id() + "-" + gallery)
                my_gallery = my_gallery_key.get()
                my_sizes.append(len(my_gallery.images))

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user': user,
            'my_user': my_user,
            'my_sizes': my_sizes,
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):

        user = users.get_current_user()
        if not user:
            return self.redirect('/error')

        my_name = self.request.get('name').strip()
        if not my_name:
            return self.redirect('/error')

        my_user_key = ndb.Key('MyUser', user.user_id())
        my_user = my_user_key.get()
        if not my_user:
            return self.redirect('/error')

        if self.request.get('+'):
            if my_name in my_user.galleries:
                return self.redirect('/error')

            my_gallery = MyGallery(id = user.user_id() + "-" + my_name)
            my_gallery.put()

            my_user.galleries.append(my_name)
            my_user.put()

        elif self.request.get('x'):
            if my_name not in my_user.galleries:
                return self.redirect('/error')

            my_gallery_key = ndb.Key('MyGallery', user.user_id() + "-" + my_name)
            my_gallery = my_gallery_key.get()
            if not my_gallery:
                return self.redirect('/error')

            for image in my_gallery.images:
                blobstore.delete(image.blob)

            my_gallery_key.delete()

            my_user.galleries.remove(my_name)
            my_user.put()

        self.redirect('/')

class GalleryPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['content-type'] = 'text/html'

        url = ''
        url_string = ''
        my_gallery = None

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

        if user:
            url = users.create_logout_url("/")
            url_string = 'logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user': user,
            'my_name': my_name,
            'my_gallery': my_gallery,
            'upload_url': blobstore.create_upload_url('/upload'),
        }

        template = JINJA_ENVIRONMENT.get_template('mygallery.html')
        self.response.write(template.render(template_values))

    def post(self):

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

        for i, image in enumerate(my_gallery.images[:]):
            if my_image != image.name:
                continue
            my_image = my_gallery.images.pop(i)
            blobstore.delete(my_image.blob)
            break

        my_gallery.put()

        self.redirect('/gallery?name=' + my_name)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/error', ErrorPage),
    ('/gallery', GalleryPage),
    ('/upload', UploadHandler),
    ('/download', DownloadHandler),
    ('/image', DownloadHandler),
])
