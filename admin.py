import logging
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from utilities import utilities
import model
import rpc


"""
    ################################################   Controller   ###############################################
""" 
class RPCMethods(rpc.RPCMethods):
    def create_album(self, sess, title, info):
        index = len(model.Album.all().fetch(20)) 
        model.Album.new(title, info, index)
        return ["ok"]
    
    def delete_album(self, sess, album):
        db.delete(album)
        order = model.Album.all().order('index').fetch(20)
        orderKeys = []
        for alb in order:
            orderKeys.append(alb.dbKey)
        return self.set_album_order(sess, orderKeys)
    
    def set_album_order(self, sess, order):
        i = 0
        for key in order:
            album = model.Album.get(key)
            album.index = i
            i = i + 1
            album.put()
        return ["ok"]
    
    def create_photo(self, sess, imageFile, caption, index):
        return
    
    def delete_photo(self, sess, photo):
        return
    
    
class RPC(rpc.RPCHandler):
    _m = RPCMethods
    
    
class AdminHandler(utilities.BaseRequestHandler):
    def get(self):
        albums = model.Album.all().order('index').fetch(20)
        self.render_to_response('templates/admin/main.html', {'albums': albums})
    
    
    
    
"""
    ################################################   Routes   ###################################################
"""
def apps_bindings():    
    apps_binding = []

    apps_binding.append(('/rpc/admin', RPC))
    apps_binding.append(('/admin', AdminHandler))
    
    return apps_binding




