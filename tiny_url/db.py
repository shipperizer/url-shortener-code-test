from uuid import uuid4
from datetime import datetime

from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError

from tiny_url.exceptions import RequestError


db = SQLAlchemy()


def db_commit():
    try:
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.error(e)
        raise RequestError


class Serializable(object):
    fields = []

    def serialize(self):
        obj = {}
        for field in [c.name for c in self.__table__.columns]:
            obj[field] = getattr(self, field)
            if isinstance(obj[field], datetime):
                obj[field] = obj[field].isoformat()
        return obj

    @classmethod
    def deserialize(cls, json_obj):
        # this is gonna block invalid keys
        obj = cls()
        cols = set([column.name for column in cls.__table__.columns])
        for field in json_obj.keys():
            if field in cols:
                setattr(obj, field, json_obj[field])
            else:
                current_app.logger.error('Unrecognized field: ', field)
        return obj


class UUIDBaseMixin(object):
    def __init__(self, *args, **kwargs):
        self.uuid = str(uuid4())
        super().__init__(*args, **kwargs)


class UUIDMixin(UUIDBaseMixin):
    uuid = db.Column(UUID, primary_key=True, default=lambda: str(uuid4()))


class Url(Serializable, UUIDMixin, db.Model):
    __tablename__ = 'url'

    url = db.Column(db.Text(), nullable=False, index=True)
    tiny_url = db.Column(db.Text(), nullable=False)
