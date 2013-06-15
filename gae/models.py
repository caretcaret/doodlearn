from google.appengine.ext import ndb


class Video(ndb.model):
    is_parent = ndb.BooleanProperty(required=True)
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    standards = ndb.StringProperty() 
    category = ndb.StringProperty(required=True)
    youtube = ndb.StringProperty(required=True)


VP_CONFUSED = 'confused'
VP_PRACTICE = 'practice'
VP_CURIOUS = 'curious'


class VideoPoint(ndb.model):
    user = ndb.UserProperty(required=True)
    video = ndb.KeyProperty(kind=Video, required=True)
    # represents the time in the video!
    time = ndb.TimeProperty(required=True)

    def _validate_point_type(prop, value):
        if value not in (VP_CURIOUS, VP_CONFUSED, VP_PRACTICE):
            raise Exception("Invalid point type, " + value)

    point_type = ndb.StringProperty(required=True, validator=_validate_point_type)