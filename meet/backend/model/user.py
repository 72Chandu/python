from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime, timezone

class User(Document):
    username = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updatedAt = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'user',
        'indexes': ['email'],
        'ordering': ['-createdAt']
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updatedAt = datetime.now(timezone.utc)

# Connect signal to auto-update updatedAt on save
from mongoengine import signals
signals.pre_save.connect(User.pre_save, sender=User)
