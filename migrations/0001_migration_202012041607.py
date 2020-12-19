# auto-generated snapshot
from peewee import *
import datetime
import peewee
import uuid


snapshot = Snapshot()


@snapshot.append
class User(peewee.Model):
    uuid = UUIDField(default=uuid.uuid4, index=True, primary_key=True)
    username = CharField(max_length=32, unique=True)
    password_hash = CharField(max_length=128)
    created = DateTimeField(default=datetime.datetime.now)
    email = CharField(max_length=128, null=True)
    mobile = CharField(max_length=11, null=True, unique=True)
    modified = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "user"


