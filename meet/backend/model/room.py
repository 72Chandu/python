# model/room.py
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, IntField
from datetime import datetime, timezone
from model.user import User  # <- adjust path to your user model file

class Room(Document):
    roomId = StringField(required=True, unique=True)
    participants = ListField(ReferenceField(User))  # stores DB User refs
    host = ReferenceField(User, null=True)
    startedAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    endedAt = DateTimeField(default=None, null=True)
    duration = IntField(default=0)
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updatedAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'room',
        'ordering': ['-startedAt'],
        'indexes': ['roomId']
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updatedAt = datetime.now(timezone.utc)

from mongoengine import signals
signals.pre_save.connect(Room.pre_save, sender=Room)
