import os

import django_settings

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class BaseRequestHandler(webapp.RequestHandler):
    """ Handles requests to the application
        todo: Catch any exceptions and log them
        All other request handlers inherit from this class"""
    def __init__(self):
        super(BaseRequestHandler, self).__init__()
        
    def template_path(self, filename):
        """Returns the full path for a template from its path relative to here."""
        return os.path.join(django_settings.PROJECT_ROOT, filename)
    
    def render_to_response(self, filename, template_args = {}):
        """Renders a Django template and sends it to the client.

        Args:
          filename: template path (relative to this file)
          template_args: argument dict for the template
        """
        filepath = self.template_path(filename)
        template_file = open(filepath) 
        compiled_template = template.Template(template_file.read()) 
        template_file.close()  
        self.response.out.write( compiled_template.render(template.Context(template_args)))
        