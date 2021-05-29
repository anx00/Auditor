import os

MONGO_USER = os.getenv('MONGO_USER', 'mongodb')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'mongodb')
MONGO_HOST = os.getenv('MONGO_HOST', '127.0.0.1')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')
MONGO_DB = os.getenv('MONGO_DB', 'mongodb')
MONGO_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE', 'admin')
