from rest_api import db
from rest_api.models.base import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = dict(extend_existing=True)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
