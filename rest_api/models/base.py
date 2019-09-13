from datetime import datetime

from rest_api import db


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.utcnow, onupdate=datetime.utcnow)
