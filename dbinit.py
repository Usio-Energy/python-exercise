from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://clement-daubrenet:postgres@localhost/usio'
db = SQLAlchemy()
db.init_app(app)


class Rates(db.Model):
    __tablename__ = 'rates'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    inserted = db.Column(DateTime(True), nullable=False, default=lambda: datetime.now(), server_default=text("now()"))
    rates = db.Column(JSON, nullable=False)


with app.app_context():
    db.create_all()
