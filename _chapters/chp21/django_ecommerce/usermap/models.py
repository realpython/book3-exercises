from mongoengine.document import Document
from mongoengine.fields import EmailField, StringField, \
    PointField, SequenceField


class UserLocation(Document):
    email = EmailField(required=True, unique=True, max_length=200)
    name = StringField(required=True, max_length=200)
    location = PointField(required=True)
    mappoint_id = SequenceField(required=True)
