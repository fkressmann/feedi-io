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
    S3_BUCKET = os.environ.get("S3_BUCKET") or 'feedio-storage'
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
    S3_BUCKET_PATH = os.environ.get("S3_BUCKET_PATH") or 'https://feedio-storage.s3.eu-central-1.amazonaws.com/'

class ProductionConfig(Config):
    FLASK_SECRET = os.environ.get("FLASK_SECRET") or '4b6e2234ffa7c9'
    DATABASE_URL = os.environ.get("DATABASE_URL_CLEAN")
    PICTURE_PATH = os.environ.get("PICTURE_PATH")
    S3_BUCKET = os.environ.get("S3_BUCKET") or 'feedio-storage'
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
    S3_BUCKET_PATH = os.environ.get("S3_BUCKET_PATH") or 'https://feedio-storage.s3.eu-central-1.amazonaws.com/'