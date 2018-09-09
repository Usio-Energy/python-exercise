from sqlalchemy import JSON, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from . import db


class Rates(db.Model):
    __tablename__ = 'rates'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    inserted = db.Column(DateTime(True), nullable=False, default=lambda: datetime.now(), server_default=text("now()"))
    rates = db.Column(JSON, nullable=False)
