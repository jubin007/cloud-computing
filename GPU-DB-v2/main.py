import datetime
from time import sleep
import urllib
import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from compare import ComparisonPage
from details import DetailsPage
from filter import FilterPage
from gpu_db import GpuEntry
from update import UpdatePage

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
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
            'gpu_entries': GpuEntry.query(),
            'msg': self.request.get('msg')
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        gpu_name = self.request.get('gpu_name')
        if ndb.Key('GpuEntry', gpu_name).get() is None:
            gpu = GpuEntry(id=self.request.get('gpu_name'))
            for param in self.request.arguments():
                if not param.startswith("gpu"):
                    continue
                try:
                    setattr(gpu, param, self.request.get(param))
                except:
                    try:
                        setattr(gpu, param, datetime.datetime.strptime(self.request.get(param), '%Y-%m-%d'))
                    except:
                        try:
                            setattr(gpu, param, True)
                        except:
                            pass
            gpu.put()
            sleep(0.25)
            msg = "New GPU [{}] created in database".format(gpu_name)
        else:
            msg = "Conflicting name [{}] with existing GPU in database".format(gpu_name)

        self.redirect("/?msg=" + msg)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/details', DetailsPage),
    ('/update', UpdatePage),
    ('/filter', FilterPage),
    ('/compare', ComparisonPage)
], debug=True)
