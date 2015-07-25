# -*- coding: utf-8 -*-
import os

MONGODB_SETTINGS = {
    'db': 'photos',
    'host': 'mongodb://Nirvana:marika@ds037262.mongolab.com:37262/photos'
}

APP_NAME = 'light-cms'
SECRET_KEY = 'secret'
SITE_NAME = 'EasyPhotos'
ADMIN_URL = '/admin/'


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
UPLOAD_URL = '/static/uploads/'


# Wechat related
wc_appid = 'appid'
wc_secret = 'secret'
wc_id = 'wc_id'
wc_token = 'wc_token'  

# Duoshuo
duoshuo_short_name = 'xxxxx'
