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
import json
import itertools
import os
import traceback

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
#from google.appengine.ext import db.GqlQuery
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
        videos = models.Video.query().fetch(limit=20)

        # http://img.youtube.com/vi/{{video}}/hqdefault.jpg for youtube pics
        values = {'videos' : videos,
                    'videos_sliced' : helper.slice_grouper(3, videos)}
        path = 'templates/index.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))

class ExploreHandler(webapp2.RequestHandler):
    def get(self):

        videos = models.Video.query().fetch()

        get_category = lambda video:video.category
        videos.sort(key=get_category)
        videos = map(lambda (k, g): list(g)[-1],itertools.groupby(videos, get_category))
        for video in videos:
            video.title = video.category
            video.link = '/category/' + video.category

        # http://img.youtube.com/vi/{{video}}/hqdefault.jpg for youtube pics
        values = {'videos' : videos, 'page_title' : 'Explore by Category'}
        path = 'templates/explore.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))


class CategoryHandler(webapp2.RequestHandler):
    def get(self, category):

        videos = models.Video.query(models.Video.category==category).fetch()

        get_category = lambda video:video.category
        videos.sort(key=get_category)
        for video in videos:
            video.title = video.name
            video.link = '/watch/' + str(video.key.id())

        # http://img.youtube.com/vi/{{video}}/hqdefault.jpg for youtube pics
        values = {'videos' : videos, 'category' : category, 'page_title' : 'Category: ' + category}
        path = 'templates/explore.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))

class WatchHandler(webapp2.RequestHandler):
    def get(self, video_id):
        video = models.Video.get_by_id(int(video_id))
        video.url = '/serve/%s' % video.video_file
        video.id = video_id
        uastring = self.request.headers.get('user_agent')
        mobile = "android" in uastring.lower()
        values = {'video': video, 'mobile' : mobile}
        path = 'templates/watch.html'
        template = JINJA_ENVIRONMENT.get_template(path)
	
        q = models.VideoPointGroup.query(models.VideoPointGroup.video == ndb.Key(models.Video, int(video_id)), models.VideoPointGroup.point_type == 'confused')
	confused_vpgs = helper.to_json(list(q.order(models.VideoPointGroup.time)))
	
        q = models.VideoPointGroup.query(models.VideoPointGroup.video == ndb.Key(models.Video, int(video_id)), models.VideoPointGroup.point_type == 'curious')
	curious_vpgs = helper.to_json(list(q.order(models.VideoPointGroup.time)))

        q = models.VideoPointGroup.query(models.VideoPointGroup.video ==  ndb.Key(models.Video, int(video_id)), models.VideoPointGroup.point_type == 'practice')
	practice_vpgs = helper.to_json(list(q.order(models.VideoPointGroup.time)))
	values = {'video' : video, 'confused_vpgs' : confused_vpgs, 'curious_vpgs' : curious_vpgs, 'practice_vpgs' : practice_vpgs}
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
    video = models.Video()
    video.name = self.request.get('name')
    video.description = self.request.get('description')
    video.category = self.request.get('category')
    video.user = users.get_current_user()

    video_blob_info = self.get_uploads('video')[0]  # 'video' is file upload field in the form
    video.video_file = video_blob_info.key()

    if self.get_uploads('thumbnail'):
        thumbnail_blob_info = self.get_uploads('thumbnail')[0]  # 'video' is file upload field in the form
        video.thumbnail_file = thumbnail_blob_info.key()

    parent = self.request.get('parent_video')
    if parent:
        video.parent_video = ndb.Key(models.Video, parent)

    video.put()
    videoPointGroup = models.VideoPointGroup.get_by_id(int(self.request.get('vpg_id')))
    
    videoPointGroup.resolved = video.key
    videoPointGroup.put()
    if self.request.get('noredirect'):
        result = {'video_id' : str(video.key.id()),
                    'video_url' : video.get_video_url()}
        self.response.write(helper.to_json(result))
    else:
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

        queryl = query.lower()

        terms = queryl.split(' ')

        def match(video):
            if queryl in video.category.lower():
                return True

            name = video.name.lower()
            for term in terms:
                if term in name:
                    return True
            return False

        videos = filter(match, models.Video.query())

        values = {'videos': videos,
                    'search' : query}
        path = 'templates/search.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(_add_default_values(values)))

class SearchAjaxHandler(webapp2.RequestHandler):
    def get(self):
        video_names = map(lambda video : video.name, models.Video.query().fetch())
        self.response.write(json.dumps(video_names))

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

class ConfusedHandler(webapp2.RequestHandler):
    def get(self):
        videos = models.Video.query().fetch()
        for video in videos:
            video.confused = 0

        videos = helper.key_results(videos)

        for vpg in models.VideoPointGroup.query():
            videos[vpg.video].confused += vpg.numberUsers

        videos = helper.unkey_results(videos)
        videos.sort(key=lambda video:video.confused, reverse=True)
        videos = videos[:6] #limit to top 5 confused

        path = 'templates/mostconfused.html'
        template = JINJA_ENVIRONMENT.get_template(path)
        values = {'videos':videos}
        self.response.write(template.render(_add_default_values(values)))


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


class ParseVideoPointHandler(webapp2.RequestHandler):

    def get(self):
        self.post()

    def post(self):
        params = self.request.get("data")
        video = self.request.get("video")

        time = self.request.get("time")
        time = int(round(float(time)))
        user = users.get_current_user()
        point_type = self.request.get("point_type")
        halfMinute = time - (time % 30)

        q = models.VideoPointGroup.query(models.VideoPointGroup.video == ndb.Key(models.Video, int(video)), models.VideoPointGroup.time == halfMinute)

        if not q.get() :
            videoPointGroup = models.VideoPointGroup()
            videoPointGroup.video = ndb.Key(models.Video, int(video))
            videoPointGroup.time = halfMinute
            videoPointGroup.numberUsers = 1
            videoPointGroup.point_type = point_type
            videoPointGroup.put()

        else:
            videoPointGroup = q.get()
            videoPointGroup.numberUsers +=1;
            videoPointGroup.put()

        #always create videopoint
        video_point = models.VideoPoint()
        video_point.user = user
        video_point.video = ndb.Key(models.Video, int(video))
        video_point.time = time
        video_point.point_type = point_type

        if videoPointGroup.resolved:
            video_point.resolved = videoPointGroup.resolved
            video_thumbnail = videoPointGroup.video.get().get_thumbnail_url()
            video_url = "/watch/"+ str(videoPointGroup.resolved.id())
            self.response.write(json.dumps({'thumbnail': video_thumbnail,
                                            'url': video_url}))
            video_point.put()
        else:
            video_point.put()
            self.response.write(json.dumps({}))

class APIListHandler(webapp2.RequestHandler):
    def get(self):
        videos = models.Video.query().fetch(limit=20)
        video_data = map(lambda v: [v.name, v.key.id(), str(v.video_file)], videos)
        self.response.write(json.dumps(video_data))
	
	def post(self):
		params = self.request.get("data")
		video = self.request.get("video")
		
		time = self.request.get("time")
		time = int(round(float(time)))
		user = users.get_current_user()	
		point_type = self.request.get("point_type")	
		halfMinute = time - (time % 30)

		q = models.VideoPointGroup.query(models.VideoPointGroup.video == ndb.Key(models.Video, int(video)), models.VideoPointGroup.time == halfMinute)

		if not q.get() :
			videoPointGroup = models.VideoPointGroup()
			videoPointGroup.video = ndb.Key(models.Video, int(video))
			videoPointGroup.time = halfMinute
			videoPointGroup.numberUsers = 1
			videoPointGroup.point_type = point_type
			videoPointGroup.put()
						
		else: 
			videoPointGroup = q.get()
			videoPointGroup.numberUsers +=1;
			videoPointGroup.put()

		#always create videopoint
		video_point = models.VideoPoint()
		video_point.user = user
		video_point.video = ndb.Key(models.Video, int(video))
		video_point.time = time
		video_point.point_type = point_type
		
		if videoPointGroup.resolved:
			video_point.resolved = videoPointGroup.resolved
			video_point.put()
			return videoPointGroup.video.get_thumbnail_url()
		video_point.put()
		self.response.out.write("hello")
		return json.dumps("{foo}")

class APIGetUploadURLHandler(webapp2.RequestHandler):
    def get(self):
        response = blobstore.create_upload_url('/upload_file')
        if self.request.get('json'):
            response = helper.to_json(response)
        self.response.write(response)
	

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create_video_point', CreateVideoPointHandler),
    ('/get_video', GetVideoHandler),
    ('/new', UploadFormHandler),
    ('/upload_file', UploadFileHandler),
    ('/serve/([^/]+)?', ServeHandler),
    ('/search', SearchHandler),
    ('/search/ajax', SearchAjaxHandler),
    ('/watch/(\d+)', WatchHandler),
    ('/parsevp',ParseVideoPointHandler),
    ('/api/list', APIListHandler),
    ('/explore', ExploreHandler),
    ('/category/(.*)', CategoryHandler),
    ('/confused', ConfusedHandler),
    ('/api/get_upload_url', APIGetUploadURLHandler)
    #('/practice', PracticeHandler),
   # ('/curious', CuriousHandler)
], debug=True)
