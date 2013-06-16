#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
##from google.appengine.ext import db.GqlQuery
from google.appengine.ext.webapp import blobstore_handlers

import webapp2

import helper
import models
import jinja2
import urllib
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

def _add_default_values(values):
    request = webapp2.get_request()
    logout_url = users.create_logout_url(request.uri)
    login_url = users.create_login_url(request.uri)

    values.update({'users' : users,
                    'logout_url' : logout_url,
                    'login_url' : login_url})

    # users.create_logout_url('/')
    return values

class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = {'videos': ['3MqYE2UuN24', 'IOYyCHGWJq4', 'KIbkoop4AYE']}
        path = 'templates/index.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))

class WatchHandler(webapp2.RequestHandler):
    def get(self, video_id):
        video = models.Video.get_by_id(int(video_id))
        video.url = '/serve/%s' % video.video_file

        values = {'video': video}
        path = 'templates/watch.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))

class CreateVideoPointHandler(webapp2.RequestHandler):
    def get(self):
        self.get()

    def post(self):
        video_point = models.VideoPoint()
        video_point.user = self.request.get('user')
        video_point.video = ndb.Key(models.Video, int(self.request.get('video')))
        video_point.time = self.request.get('time')
        video_point.point_type = self.request.get('point_type')
        video_point.put()

        self.response.write('success')

class GetVideoHandler(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        video = models.Video.get_by_id(int(self.request.get('video')))

        self.response.write(helper.to_json(video))

class UploadFormHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload_file')

    values = {'upload_url': upload_url}
    path = 'templates/upload.html'
    template = JINJA_ENVIRONMENT.get_template(path)
    self.response.write(template.render(_add_default_values(values)))

class UploadFileHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]

    video = models.Video()
    video.name = self.request.get('name')
    video.description = self.request.get('description')
    video.category = self.request.get('category')
    video.video_file = blob_info.key()
    video.user = users.get_current_user()

    parent = self.request.get('parent')
    if parent:
        video.parent_video = ndb.Key(models.Video, self.request.get('parent'))

    video.put()

    # TODO: display a success page?
    self.redirect('/watch/' + str(video.key.id()))

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        query = self.request.get('search')
        if not query:
            query = ''
        videos_q = models.Video.gql("WHERE category = :1", query)
        videos = list(videos_q)
        values = {'videos': videos}
        path = 'templates/search.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        query = self.request.get('search')
        if not query:
            query = ''
        videos_q = models.Video.gql("WHERE category = :1", query)
        videos = list(videos_q)
        values = {'videos': videos}
        path = 'templates/search.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))
'''
class ConfusedHandler(webapp2.RequestHandler):
	def get(self):
		videoGroups = GqlQuery("SELECT * FROM VideoPointGroup WHERE point_type = 'confused' ORDERBY numberUsers DESC LIMIT 20")
		path = 'templates/index.html'
		template = JINJA_ENVIRONMENT.get_template(path)
		values = {'videos':videoGroups}
		self.response.write(template.render(values))	

class PracticeHandler(webapp2.RequestHandler):
	def get(self):
		videoGroups = GqlQuery("SELECT * FROM VideoPointGroup WHERE point_type = 'practice' ORDERBY numberUsers DESC LIMIT 20")
		path = 'templates/index.html'
		template = JINJA_ENVIRONMENT.get_template(path)
		values = {'videos':videoGroups}
		self.response.write(template.render(values))	

class CuriousHandler(webapp2.RequestHandler):
	def get(self):
		videoGroups = GqlQuery("SELECT * FROM VideoPointGroup WHERE point_type = 'curious' ORDERBY numberUsers DESC LIMIT 20")
		path = 'templates/index.html'
		template = JINJA_ENVIRONMENT.get_template(path)
		values = {'videos':videoGroups}
		self.response.write(template.render(values))	
'''

class ParseVideoPoint(webapp2.RequestHandler):
	def post(self):
		params = self.request.get("data")
		
		jsonDict = json.loads(params);
		
		videoPointGroup = models.VideoPointGroup()
		
		halfMinute = jsonDict['time'] / 30;

		q = models.VideoPointGroup.query(models.VideoPointGroup.video == ndb.Key(models.Video, int(jsonDict['video'])), models.VideoPointGroup.time == halfMinute)

		if not q.hasNext() :
			videoPointGroup.video = ndb.Key(models.Video, int(jsonDict['video']))
			videoPointGroup.time = halfMinute
			videoPointGroup.numberUsers = 1
			videoPointGroup.point_type = jsonDict['point_type']
						
		else: 
			videoPointGroup = q.next()
			videoPointGroup.numberUsers +=1;
			videoPointGroup.put()
			return videoPointGroup.video

		#always create videopoint
		video_point = models.VideoPoint()
		video_point.user = jsonDict['user']
		video_point.video = ndb.Key(models.Video, int(jsonDict['video']))
		video_point.time = jsonDict['time']
		video_point.point_type = jsonDict['point_type']
		video_point.put()
	

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create_video_point', CreateVideoPointHandler),
    ('/get_video', GetVideoHandler),
    ('/new', UploadFormHandler),
    ('/upload_file', UploadFileHandler),
    ('/serve/([^/]+)?', ServeHandler),
    ('/search', SearchHandler),
    ('/watch/(\d+)', WatchHandler)
    #('/confused', ConfusedHandler),
    #('/practice', PracticeHandler),
   # ('/curious', CuriousHandler)
], debug=True)
