from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class TfTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(80), unique=False, nullable=False)
    tf = db.Column(db.Float, nullable=False)
    file_name = db.Column(db.String(80), nullable=False)


class IdfTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(80), unique=False, nullable=False)
    idf = db.Column(db.Float, nullable=False)


def init_db():
    db.create_all()
    print('OK')