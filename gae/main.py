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

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import webapp2

import helper
import models
import jinja2
import urllib

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = {'videos': ['3MqYE2UuN24', 'IOYyCHGWJq4', 'KIbkoop4AYE']}
        path = 'templates/index.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(values))

class WatchHandler(webapp2.RequestHandler):
    def get(self, video):
        values = {'youtube_link': video}
        path = 'templates/watch.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(values))

class CreateVideoHandler(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
  #   	params = dict(self.request.params.items())

  #   	model_type = params.pop("model", None)
  #   	model = None
  #   	if model_type == 'video':
  #   		model = models.Video
		# elif model_type == 'video_point':
		# 	model = models.VideoPoint
		# else:
		# 	raise Exception("unknown model type")

  #   	model = model(**params)
  #   	model.put()
        
        video = models.Video()
        video.name = self.request.get('name')

        parent = self.request.get('parent')
        if parent:
        	video.parent_video = ndb.Key(models.Video, self.request.get('parent'))

        video.description = self.request.get('description')
        video.standards = self.request.get('standards')
        video.category = self.request.get('category')
        video.youtube = self.request.get('youtube')
        video.put()

        self.response.write('success')

class CreateVideoPointHandler(webapp2.RequestHandler):
    def get(self):
        self.get()

    def post(self):
        video_point = models.VideoPoint()
        video_point.user = self.request.get('user')
        video_point.video = ndb.Key(models.VideoPoint, int(self.request.get('video')))
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
    self.response.write(template.render(values))

class UploadFileHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.redirect('/serve/%s' % blob_info.key())

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
        self.response.write(template.render(values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create', CreateVideoHandler),
    ('/create_video_point', CreateVideoPointHandler),
    ('/get_video', GetVideoHandler),
    ('/upload', UploadFormHandler),
    ('/upload_file', UploadFileHandler),
    ('/serve/([^/]+)?', ServeHandler),
    ('/search', SearchHandler),
    ('/watch/(.+)', WatchHandler)
], debug=True)
