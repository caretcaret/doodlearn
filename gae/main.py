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
from google.appengine.ext import ndb

import webapp2

import helper
import models
import jinja2
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

import os
import urllib

import jinja2
import webapp2

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
    ('/search', SearchHandler),
    ('/watch/(.+)', WatchHandler)
], debug=True)
