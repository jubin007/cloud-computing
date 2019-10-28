import datetime
from time import sleep
import urllib
import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from gpu_db import GpuEntry

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ComparisonPage(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'gpu_one': ndb.Key('GpuEntry', self.request.get('gpu_one')).get(),
            'gpu_two': ndb.Key('GpuEntry', self.request.get('gpu_two')).get(),
        }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))
