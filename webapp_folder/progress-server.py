#!/usr/bin/env python
# -*- coding: latin-1 -*-

Site = 'People . Elkhorn.io'

Timezone = 'Pacific/Honolulu'


  # - System
import os
import cgi
import urllib
import wsgiref.handlers
import datetime
import json, ast
import sys,imp
  # - Appengine
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api import images
from urlparse import urlparse
  # -
from google.appengine.ext import ndb
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app


import _html as _html





#----------------------------------------------#
#        Completed Data Stucture               #
#----------------------------------------------#
class People_db(ndb.Model):
    data_id = ndb.StringProperty()
#
    user_id = ndb.StringProperty()
    user_email = ndb.StringProperty()
#
    item_id = ndb.StringProperty()
    item_name = ndb.StringProperty()
    item_kind = ndb.StringProperty()
#
    item_status = ndb.StringProperty()
    status_date = ndb.StringProperty()

    @classmethod
    def _get_my_status(self):
      client_email = users.get_current_user().email()
      q = People_db.query(People_db.user_email == client_email)
      db_data = []
      for item in q.iter():
        db_data.append(item.to_dict(exclude=['user_id','user_email']))
      return json.dumps(db_data)


class updatePeople_db(webapp2.RequestHandler):
  def post(self):
    page_address = self.request.uri
    base = os.path.basename(page_address)
    
    user = users.get_current_user()
    if user:
        item_id = self.request.get('item_id')
        client_email = user.email()
        key_name = item_id + '_' + client_email
        item = People_db.get_by_id(key_name)
        
        if not item:
            item = People_db(id=key_name)
        
        item.user_id = user.user_id()
        item.user_email = user.email()
        item.status_date = datetime.datetime.now(pytz.timezone(Timezone)).strftime("%Y/%m/%d %H:%M:%S")
        

        item.item_id = self.request.get('item_id')
        item.item_name = self.request.get('item_name')
        item.item_kind = self.request.get('item_kind')
        item.item_status = self.request.get('item_status')

        item.put()
        
    self.redirect('/my_info')




#----------------------------------------------#
#        Completed Data Stucture               #
#----------------------------------------------#
class Progress_db(ndb.Model):
    data_id = ndb.StringProperty()
#
    user_id = ndb.StringProperty()
    user_email = ndb.StringProperty()
#
    item_id = ndb.StringProperty()
    item_name = ndb.StringProperty()
    item_kind = ndb.StringProperty()
#
    item_status = ndb.StringProperty()
    status_date = ndb.StringProperty()

    @classmethod
    def _get_my_status(self):
      client_email = users.get_current_user().email()
      q = People_db.query(People_db.user_email == client_email)
      db_data = []
      for item in q.iter():
        db_data.append(item.to_dict(exclude=['user_id','user_email']))
      return json.dumps(db_data)


class updateProgress_db(webapp2.RequestHandler):
  def post(self):
    page_address = self.request.uri
    base = os.path.basename(page_address)
    
    user = users.get_current_user()
    if user:
        item_id = self.request.get('item_id')
        client_email = user.email()
        key_name = item_id + '_' + client_email
        item = People_db.get_by_id(key_name)
        
        if not item:
            item = People_db(id=key_name)
        
        item.user_id = user.user_id()
        item.user_email = user.email()
        item.status_date = datetime.datetime.now(pytz.timezone(Timezone)).strftime("%Y/%m/%d %H:%M:%S")
        

        item.item_id = self.request.get('item_id')
        item.item_name = self.request.get('item_name')
        item.item_kind = self.request.get('item_kind')
        item.item_status = self.request.get('item_status')

        item.put()
        
    self.redirect('/my_info')






class publicSite(webapp2.RequestHandler):
    def get(self):
      # - URL Parse
        page_address = self.request.uri
        uri = urlparse(page_address)
        path = uri[2] # - uri.path
        layers = path.split('/')
        path_layer = layers[1]
        base = os.path.basename(page_address)
      # - user
        user = users.get_current_user()
        if users.get_current_user(): # - logged in
          login_key = users.create_logout_url(self.request.uri)
          gate = 'Sign out'
          user_name = user.nickname()
        else: # - logged out
          login_key = users.create_login_url(self.request.uri)
          gate = 'Sign in'
          user_name = 'No User'
      # - app data
      
        html_file = 'main_layout.html'

        page_html = _html.front_page
        page_id = ''
        page_name = 'Front Page'
        nav_select = ''
        
        
      # -
        if path_layer == 'my_info':
            page_html = _html.user_page + _html.account_page
            page_id = 'my_info'
            page_name = 'My Info'
            nav_select = 'my_info'
            user_header = 'on'


      # - template
        objects = {

            'login_key': login_key,
            'gate': gate,
            'user_name': user_name,
        
            'page_id': page_id,
            'page_name': page_name,
            'nav_select': nav_select,
        
            'page_html': page_html,
        
        
        
        }
      # - render
        path = os.path.join(os.path.dirname(__file__), 'html/%s' %html_file)
        self.response.out.write(template.render(path, objects))




app = webapp2.WSGIApplication([    # - Pages
    ('/', publicSite),
    
    ('/my_info', publicSite),
    ('/my_progress', publicSite),
    
    ('/add_people', updatePeople_db),
    
    ('/add_progress', updateProgress_db),
    
    
    ('/site_people', publicSite),
  

], debug=True)
