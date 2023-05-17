class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://localhost:5432/music_library"
    SQLALCHEMY_TEST_DATABASE_URI = "postgresql+psycopg2://localhost:5432/test"
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    FLASK_ADMIN_SWATCH = 'cerulean'
    SECURITY_PASSWORD_SALT = 'secret_salt'
    DB_HOST = 'localhost'
    DB_NAME = 'music_library'
    DB_USER = 'postgres'
    DB_PASS = 'postgres'
