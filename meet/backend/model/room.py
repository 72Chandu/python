from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, IntField
from datetime import datetime, timezone
from user import user  # Assuming you have this defined elsewhere

class Room(Document):
    roomId = StringField(required=True, unique=True)
    participants = ListField(ReferenceField(user))
    host = ReferenceField(user)
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
