import django_set_version
import simplejson
import logging
import datetime

from utilities.utilities import BaseRequestHandler

class RPCMethods(object):
    """ Defines the methods that can be RPCed. """
    def Add(self, *args):
        # The JSON encoding may have encoded integers as strings.
        # Be sure to convert args to any mandatory type(s).
        ints = [int(arg) for arg in args]
        return sum(ints)
    def Date(self, *args):
        return datetime.datetime.now().strftime("%m/%d/%y %H:%M")

    def Echo(self, *args):
        ans = '<br />'.join([args[0], args[1]])
        return ans

class RPCHandler(BaseRequestHandler):
    """ Allows the functions defined in the RPCMethods class to be RPCed."""
    _m = RPCMethods
    def __init__(self):
        super(RPCHandler, self).__init__()
        self.methods = self._m()
     
    def get(self):
        self.error(403) # access denied
        return

    def post(self):
        func = self.request.get('func')
        if not func:
            self.error(403) # access denied
            return
        args = simplejson.loads(self.request.get('args'))
        logging.info('Func: %s, Args: %s', func, args)
        
        if func[0] == '_':
            self.error(403) # access denied
            return
         
        func = getattr(self.methods, func, None)
        if not func:
            self.error(404)
            return
    
        result = func(self, *args)
        self.response.out.write(simplejson.dumps(result))
