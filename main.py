import django_set_version
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("<html><body>")
        self.response.out.write("<p>Welcome to iantom.com!</p>")
        self.response.out.write("</body></html>")

def main():
    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG)
    
    apps_binding = []
    
    apps_binding.append(('/', MainHandler))
    
    
    application = webapp.WSGIApplication(apps_binding, debug=True)
    
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
