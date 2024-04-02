import os
import secrets
import pathlib


class Config:
    UPLOAD_PATH = 'uploads'
    SECRET_KEY = secrets.token_hex()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(pathlib.Path.cwd(), 'words.db')
