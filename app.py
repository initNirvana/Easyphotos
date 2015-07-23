# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(1, os.path.join(os.path.abspath("."),'env/lib/python2.7/site-packages'))
sys.path.insert(1, os.path.join(os.path.abspath("."),'lib/'))
sys.path.insert(0,'lib')
from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
vendor.add('env/lib/python2.7/site-packages')

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.bcrypt import Bcrypt
from flask.ext import login
from flask.ext.babelex import Babel
import settings


app = Flask(settings.APP_NAME)
app.config.from_object(settings)

login_manager = login.LoginManager()

app.config['BCRYPT_LOG_ROUNDS'] = 1


db = MongoEngine(app)
bcrypt = Bcrypt(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'en_AU'
