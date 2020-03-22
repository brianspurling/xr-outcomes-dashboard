import os

import environ
env = environ.Env()
environ.Env.read_env()  # reads the .env file

# If S3 is not configured in environment, set to empty string (and app will attempt to load from CSV)
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
S3_BUCKET = env('S3_BUCKET', default='')
