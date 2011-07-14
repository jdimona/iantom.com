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
    index = db.IntegerProperty()
    @classmethod
    def new(cls, newTitle, newInfo, newIndex, newPhotos = []):
        super(Album, cls).new(title = newTitle, info = newInfo, index = newIndex, photos = newPhotos)
    
class Photo(dbRoot):
    image = blobstore.BlobReferenceProperty()
    caption = db.StringProperty()
    index = db.IntegerProperty()
    @classmethod
    def new(cls, newImage, newCaption, newIndex):
        super(Album, cls).new(image = newImage, caption = newCaption, index = newIndex)
    



"""
    ################################################   Controller   ###############################################
""" 
class RPCMethods(rpc.RPCMethods):
    def get_main(self, sess):
        return
    
    def get_about(self, sess):
        return
    
    def get_albums(self, sess):
        return
    
    def get_photo(self, sess, album, index):
        return
    
    def create_album(self, sess, title, info, index):
        return
    
    def delete_album(self, sess, album):
        return
    
    def create_photo(self, sess, imageFile, caption, index):
        return
    
    def delete_photo(self, sess, photo):
        return


class RPC(rpc.RPCHandler):
    _m = RPCMethods



"""
    ################################################   Routes   ###################################################
"""
def apps_bindings():    
    apps_binding = []

    apps_binding.append(('/rpc/portfolio', RPC))
    
    return apps_binding



