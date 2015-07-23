# -*- coding:utf-8 -*-
from app import app, login_manager
from flask.ext.admin import Admin
from flask.ext.admin.contrib.fileadmin import FileAdmin
from views import light_cms
from wc import wc
from admin_views import UserView, IndexView, GeneralView
from models import User, Image, Gallery
import settings


login_manager.init_app(app)

app.register_blueprint(light_cms)
app.register_blueprint(wc)

admin = Admin(app, name="{}관리".format(settings.SITE_NAME), index_view=IndexView(endpoint='admin'))
admin.add_view(UserView(User, name='회원'))
admin.add_view(FileAdmin(settings.UPLOAD_FOLDER, settings.UPLOAD_URL, name='upload'))
admin.add_view(GeneralView(Image, name='사진'))
admin.add_view(GeneralView(Gallery, name='앨범'))
