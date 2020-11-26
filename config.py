import os


class Config:
    """
      Base Configuration class will contain most of the basic configuration attributes and will be changed accordingly
      based on the environment.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'