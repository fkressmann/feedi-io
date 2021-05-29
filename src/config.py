import os

FLASK_SECRET = os.environ.get("FLASK_SECRET") or '4b6e2234ffa7c9'
DB_HOST = os.environ.get("DB_HOST") or 'localhost'
DB_PASSWORD = os.environ.get("DB_PASSWORD") or 'SuperPasswort!'
DB_USER = os.environ.get("DB_USER") or 'feedi-io'
DB_NAME = os.environ.get("DB_NAME") or 'feedi-io'
OWN_HOSTNAME = os.environ.get("OWN_HOSTNAME")
