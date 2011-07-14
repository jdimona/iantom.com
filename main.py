#!/usr/bin/env python

import django_set_version
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from utilities import utilities
import model

class MainHandler(utilities.BaseRequestHandler):
    def get(self):
        albums = model.Album.all().order('-index').fetch(15)
        self.render_to_response('templates/main.html', {'albums': albums})

def main():
    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG)
    
    apps_binding = []
    
    apps_binding.append(('/', MainHandler))
    apps_binding.extend(model.apps_bindings())
    
    
    application = webapp.WSGIApplication(apps_binding, debug=True)
    
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
