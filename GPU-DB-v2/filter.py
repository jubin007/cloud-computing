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


class FilterPage(webapp2.RequestHandler):
    def get(self):
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
            'gpu_entries': GpuEntry.query()
        }
        template = JINJA_ENVIRONMENT.get_template('filter.html')
        self.response.write(template.render(template_values))

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
            'user': user
        }

        gpu_entries = GpuEntry.query()
        for param in self.request.arguments():
            if not param.startswith("gpu"):
                continue
            try:
                template_values[param] = True
                gpu_entries = gpu_entries.filter(getattr(GpuEntry, param) == True)
            except:
                pass
        template_values['gpu_entries'] = gpu_entries

        template = JINJA_ENVIRONMENT.get_template('filter.html')
        self.response.write(template.render(template_values))
