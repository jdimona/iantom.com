#!/usr/bin/env python

import django_set_version
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import utilities

class MainHandler(utilities.BaseRequestHandler):
    def get(self):
        self.render_to_response('templates/main.html')

def main():
    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG)
    
    apps_binding = []
    
    apps_binding.append(('/', MainHandler))
    
    
    application = webapp.WSGIApplication(apps_binding, debug=True)
    
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
