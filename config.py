import os


class Config:
    """
      Base Configuration class will contain most of the basic configuration attributes and will be changed accordingly
      based on the environment.
    """
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'