import os

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or "YOU NEVER GUESS"
    #SECRET_KEY="YOU NEVER GUESS"