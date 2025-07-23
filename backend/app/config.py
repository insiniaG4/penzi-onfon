

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://penzi_user:penzi123@db/penzi_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
