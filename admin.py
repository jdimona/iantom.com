import logging
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
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
    
    def delete_album(self, sess, albumKey):
        album = model.Album.get(albumKey)
        photos = model.Photo.get(album.photos)
        for photo in photos:
            blobstore.BlobInfo.get(photo.image.key()).delete()
            db.delete(photo.dbKey)
        db.delete(albumKey)
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
    
    def show_album(self, sess, albumKey):
        upload_url = blobstore.create_upload_url('/admin/newslide')
        album = model.Album.get(albumKey)
        photo_list = []
        if album.numPhotos > 0:
            photos = sorted(model.Photo.get(album.photos), key=lambda photo: photo.index)
            for photo in photos:
                if photo.textOnly:
                    photo_list.append({
                                       'textOnly': photo.textOnly,
                                       'caption': photo.caption, 
                                       'dbKey': photo.dbKey
                                       })
                else:
                    photo_list.append({
                                       'textOnly': photo.textOnly,
                                       'caption': photo.caption, 
                                       'dbKey': photo.dbKey, 
                                       'picUrl': images.get_serving_url(photo.image, 150)
                                       })
        templ = sess.template_path('templates/admin/album-display.html')
        html = template.render(templ, {'slides': photo_list, 'upload_url': upload_url})
        return html
    
    def delete_photo(self, sess, photoKey, albumKey):
        album = model.Album.get(albumKey)
        photo = model.Photo.get(photoKey)
        blobstore.BlobInfo.get(photo.image.key()).delete()
        db.delete(photoKey)
        logging.debug('Photo Key: %s, album.photos[0]: %s', photoKey, album.photos[0])
        newPhotos = []
        for photo in album.photos:
            if photo != photoKey:
                newPhotos.append(photo)
        
        album.photos = newPhotos
        album.numPhotos = album.numPhotos - 1
        album.put()
        if album.numPhotos > 0:
            photos = sorted(model.Photo.get(album.photos), key=lambda photo: photo.index)
            return self.set_photo_order(sess, photos)
        return ["ok"]
    
    def set_photo_order(self, sess, order):
        i = 0
        for key in order:
            photo = model.Photo.get(key)
            photo.index = i
            i = i + 1
            photo.put()
        return ["ok"]
    
    
class RPC(rpc.RPCHandler):
    _m = RPCMethods
    
    
class AdminHandler(utilities.BaseRequestHandler):
    def get(self):
        albums = model.Album.all().order('index').fetch(20)
        self.render_to_response('templates/admin/main.html', {'albums': albums})
    
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        album = model.Album.get(self.request.get('albumKey'))
        index = len(model.Photo.all().fetch(50))
        caption = self.request.get('caption')
        if self.request.get('textOnly') == "true":
            textOnly = True
            model.Photo.new(caption, textOnly, index)
        else:
            textOnly = False
            upload_files = self.get_uploads('file')
            blob_info = upload_files[0]
            image = blob_info.key()
            model.Photo.new(caption, textOnly, index, image)
            
        photo = model.Photo.all().order('-index').get()
        album.photos.append(photo.key())
        album.numPhotos = album.numPhotos + 1
        album.put()
        
        self.redirect('/admin')
    
    
"""
    ################################################   Routes   ###################################################
"""
def apps_bindings():    
    apps_binding = []

    apps_binding.append(('/rpc/admin', RPC))
    apps_binding.append(('/admin', AdminHandler))
    apps_binding.append(('/admin/newslide', UploadHandler))
    
    return apps_binding




