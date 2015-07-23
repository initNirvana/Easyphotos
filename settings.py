# -*- coding: utf-8 -*-
import os

MONGODB_SETTINGS = {
    'db': 'photos',  # Name of the database, other available settings refer to Mongoengine documentation
    'host': 'mongodb://Nirvana:marika@ds037262.mongolab.com:37262/photos'
}

APP_NAME = 'light-cms'  # English Only
SECRET_KEY = 'secret'  # Change this in production
SITE_NAME = 'EasyPhotos'
ADMIN_URL = '/admin/'  # I forgot where I used it


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
UPLOAD_URL = '/static/uploads/'


# Wechat related
wc_appid = 'appid'
wc_secret = 'secret'
wc_id = 'wc_id'  # Wechat public account id (the one you set, NOT the original id)
wc_token = 'wc_token'  # Wechat public

# Duoshuo
duoshuo_short_name = 'xxxxx'
