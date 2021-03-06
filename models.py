from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    api_name = db.Column(db.String(), nullable=False)
    config_tag = db.Column(db.String, nullable=False, unique=True)
    current_config = db.Column(db.String(), nullable=False)
    previous_config = db.Column(db.String(), nullable=True)
    default_config = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return "Config <{id}: {api_name}>".format(id=self.id, api_name=self.api_name)

    __repr__ = __str__


class ConfigSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Config
        sqla_session = db.session

config_schema = ConfigSchema()
config_schema_many = ConfigSchema(many=True)
