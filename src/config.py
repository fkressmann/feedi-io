import os

class Config(object):
    TESTING = False

class DevelopmentConfig(Config):
    FLASK_SECRET = os.environ.get("FLASK_SECRET") or '4b6e2234ffa7c9'
    DB_HOST = os.environ.get("DB_HOST") or 'localhost'
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or 'SuperPasswort!'
    DB_USER = os.environ.get("DB_USER") or 'feedi_io'
    DB_NAME = os.environ.get("DB_NAME") or 'feedi_io'
    PICTURE_PATH = os.environ.get("PICTURE_PATH") or 'pics/'

class ProductionConfig(Config):
    FLASK_SECRET = os.environ.get("FLASK_SECRET") or '4b6e2234ffa7c9'
    DATABASE_URL = os.environ.get("DATABASE_URL")