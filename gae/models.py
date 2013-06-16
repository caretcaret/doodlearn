from google.appengine.ext import ndb


class Video(ndb.Model):
    user = ndb.UserProperty()
    parent_video = ndb.KeyProperty(kind='Video',default=None)
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    standards = ndb.StringProperty() 
    category = ndb.StringProperty(required=True)
    video_file = ndb.BlobKeyProperty(required=True)
    def get_video_url(self):
        if self.video_file:
            return '/serve/%s' % self.video_file
        else:
            return None

    thumbnail_file = ndb.BlobKeyProperty()
    def get_thumbnail_url(self):
        if self.thumbnail_file:
            return '/serve/%s' % self.thumbnail_file
        else:
            return '/static/img/placeholder.png'

    def get_view_url(self):
        if self.key.id():
            return '/watch/' + str(self.key.id())
        else:
            return None


VP_CONFUSED = 'confused'
VP_PRACTICE = 'practice'
VP_CURIOUS = 'curious'


class VideoPoint(ndb.Model):
    user = ndb.UserProperty(required=True)
    video = ndb.KeyProperty(kind='Video', required=True)
    # represents the time in the video!
    time = ndb.IntegerProperty(required=True)
    resolved = ndb.KeyProperty(kind='Video')

    def _validate_point_type(prop, value):
        if value not in (VP_CURIOUS, VP_CONFUSED, VP_PRACTICE):
            raise Exception("Invalid point type, " + value)

    point_type = ndb.StringProperty(required=True, validator=_validate_point_type)


class VideoPointGroup(ndb.Model):
	video = ndb.KeyProperty(kind='Video', required=True)
	time = ndb.IntegerProperty(required=True)
	resolved = ndb.KeyProperty(kind='Video')
	numberUsers = ndb.IntegerProperty(required=True)
	def _validate_point_type(prop, value):
		if value not in (VP_CURIOUS, VP_CONFUSED, VP_PRACTICE):
			raise Exception("Invalid point type, " + value)

	point_type = ndb.StringProperty(required=True, validator=_validate_point_type)
