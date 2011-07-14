import os

import django_settings

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

import uuid

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
        
class UrlEncoder(object):
    def __init__(self):
        self.alphabet = 'JedR8LNFY2j6MrhkBSADUyfP5amuH9xQCX4VqbgpsGtnW7vc3TwKE'
        block_size = 22
        self.block_size = block_size
        self.mask = (1 << block_size) - 1
        self.mapping = range(block_size)
        self.mapping.reverse()
    def encode_url(self, n, min_length = 0):
        return self.enbase(self.encode(n), min_length)
    def decode_url(self, n):
        return self.decode(self.debase(n))
    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)
    def _encode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << i):
                result |= (1 << b)
        return result
    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)
    def _decode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << b):
                result |= (1 << i)
        return result
    def enbase(self, x, min_length = 0):
        result = self._enbase(x)
        padding = self.alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)
    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self.enbase(x / n) + self.alphabet[x % n]
    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            result += self.alphabet.index(c) * (n ** i)
        return result

def getUUID():
    """
    Return an encoded system-wide unique ID
    """
    theEncoder = UrlEncoder()
    return theEncoder.enbase(theEncoder.encode(uuid.uuid4().int))
