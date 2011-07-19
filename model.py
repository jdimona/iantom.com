import logging
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from utilities import utilities
import rpc





"""
    ################################################   Model   ####################################################
"""
class dbRoot(db.Model):
    created = db.DateTimeProperty(auto_now_add = True)
    changed = db.DateTimeProperty(auto_now = True)
    updated = property(lambda s: str(s.changed.strftime('%a, %d %b %Y %H:%M')))        
    started = property(lambda s: str(s.created.strftime('%d %b %Y')))
    dbKey = property(lambda s: str(s.key()))
    @classmethod
    def new(cls, **kwargs):
        key_name = utilities.getUUID()
        obj = cls.get_or_insert(key_name = key_name, **kwargs)
        obj.put()
        return obj

class Album(dbRoot):
    title = db.StringProperty()
    info = db.StringProperty()
    photos = db.ListProperty(db.Key)
    numPhotos = db.IntegerProperty()
    index = db.IntegerProperty()
    @classmethod
    def new(cls, newTitle, newInfo, newIndex, newNumPhotos = 0, newPhotos = []):
        super(Album, cls).new(title = newTitle, info = newInfo, index = newIndex, numPhotos = newNumPhotos, photos = newPhotos)
    
class Photo(dbRoot):
    image = blobstore.BlobReferenceProperty()
    caption = db.StringProperty()
    textOnly = db.BooleanProperty()
    index = db.IntegerProperty()
    @classmethod
    def new(cls, newCaption, newTextOnly, newIndex, newImage = None):
        super(Photo, cls).new(caption = newCaption, textOnly = newTextOnly, index = newIndex, image = newImage)
    



"""
    ################################################   Controller   ###############################################
""" 
class RPCMethods(rpc.RPCMethods):
    def get_main(self, sess):
        templ = sess.template_path('templates/photo.html')
        html = template.render(templ, {})
        return html
    
    def get_about(self, sess):
        templ = sess.template_path('templates/text.html')
        html = template.render(templ, {})
        return html
    
    def get_photo(self, sess, album, index):
        return "hi", 10
    

class RPC(rpc.RPCHandler):
    _m = RPCMethods




"""
    ################################################   Routes   ###################################################
"""
def apps_bindings():    
    apps_binding = []

    apps_binding.append(('/rpc/portfolio', RPC))
    
    return apps_binding



