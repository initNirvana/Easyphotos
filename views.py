from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from flask.ext import login
from app import login_manager
from models import User, Image, Gallery
import shortuuid
import settings

light_cms = Blueprint('light-cms', __name__, template_folder='templates')
system_user, _ = User.objects.get_or_create(username='SYSTEM', email='1@1.com', active=False)

view = False
from functools import wraps

def not_yet(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if view is False:
            return redirect('404')
        return f(*args, **kwargs)
    return decorated_function


@light_cms.route('/404')
def page():
    return render_template('404.html')

@light_cms.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@light_cms.route('/')
def index():
    return render_template('index.html',
                           title='홈',
                           images=Image.objects(gallery__not__exists=True).order_by('-pub_date')[:30],
                           galleries=Gallery.objects().order_by('-pub_date'),
                           )


@light_cms.route('/images/')
@light_cms.route('/images/page/<int:page>/')
def square(page=1):
    return render_template('list.html',
                           title='사진모음',
                           images=Image.objects(gallery__not__exists=True).order_by('-pub_date').paginate(page=page,
                                                                                                          per_page=30),
                           wall_title='모든 사진',
                           )


@light_cms.route('/tag/<tag>/')
@light_cms.route('/tag/<tag>/page/<int:page>/')
def tag_view(tag, page=1):
    images = Image.objects(tags=tag)
    return render_template('tag_picture_list.html',
                           title=tag,
                           images=images.order_by('-pub_date').paginate(page=page, per_page=30),
                           wall_title='tag: %s 모든 사진' % tag,
                           tag=tag,
                           )


@light_cms.route('/user/<username>/')
@light_cms.route('/user/<username>/page/<int:page>/')
def user_picture(username, page=1):
    u = User.objects.get(username=username)
    images = Image.objects(user=u)
    return render_template('user_image_list.html',
                           title='%s 모든사진' % username,
                           images=images.order_by('-pub_date').paginate(page=page, per_page=30),
                           wall_title='%s 모든사진' % username,
                           username=username,
                           )


@light_cms.route('/login/', methods=['GET', 'POST'])
@not_yet
def user_login():
    if request.method == 'GET':
        login.logout_user()
        return render_template('login.html', title='회원가입')
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if (not username) or (not password):
            flash('회원이름과 비밀번호를 공백으로 할수는 없습니다.', 'info')
            return redirect(url_for('light-cms.user_login'))
        u = User.objects(username=username).first()
        if not u:
            flash('회원 이름이 존재하지 않습니다', 'warning')
            return redirect(url_for('light-cms.user_login'))
        if u.check_password(password):
            login.login_user(u, remember=True)
            flash('로그인 성공', 'success')
            return redirect(url_for('light-cms.index'))
        else:
            flash('잘못된 암호', 'warning')
            return redirect(url_for('light-cms.user_login'))


@light_cms.route('/reg/', methods=['GET', 'POST'])
@not_yet
def user_reg():
    if request.method == 'GET':
        login.logout_user()
        return render_template('reg.html', title='회원가입')
    if request.method == 'POST':
        username, password, email = request.form['username'], request.form['password'], request.form['email']
        if (not username) or (not password) or (not email):
            flash('회원 이름과 비밀번호를 공백으로 할수는 없습니다', 'info')
            return redirect(url_for('light-cms.user_reg'))
        u = User.objects(username=username).first()
        if u:
            flash('회원 이름이 이미 존재합니다', 'warning')
            return redirect(url_for('light-cms.user_reg'))
        if ('@' not in email) or (email.endswith('.')):
            flash('E-Mail 이상', 'warning')
            return redirect(url_for('light-cms.user_reg'))
        u = User(username=username, email=email, password=password)
        u.save()
        login.login_user(u, remember=True)
        return redirect(url_for('light-cms.index'))


@light_cms.route('/i/<iid>/', methods=['GET', 'POST'])
def image(iid):
    i = Image.objects.get_or_404(iid=iid)
    if request.method == 'GET':
        return render_template('image.html', image=i, title=i.title)


@light_cms.route('/p/<iid>/')
def display_image(iid):
    i = Image.objects.get_or_404(iid=iid)
    return Response(i.image.read(), mimetype='image')


@light_cms.route('/thumb/<iid>/')
def display_thumbnail(iid):
    i = Image.objects.get_or_404(iid=iid)
    return Response(i.image.thumbnail.read(), mimetype='image')


@light_cms.route('/i/<iid>/edit/', methods=['GET', 'POST'])
@not_yet
def edit_image(iid):
    i = Image.objects.get_or_404(iid=iid)
    if i.user.username != login.current_user.username:
        return redirect(url_for('.image', iid=iid))
    if request.method == 'GET':
        return render_template('edit.html', title='사진 편집', image=i)
    if request.method == 'POST':
        form = request.form
        title, desc, tags = form['title'], form['desc'], form['tags']
        tags = tags.split()
        i.title = title
        i.description = desc
        i.tags = tags
        i.save()
        return redirect(url_for('.image', iid=iid))


@light_cms.route('/i/<iid>/claim/')
@not_yet
def claim_image(iid):
    i = Image.objects.get_or_404(iid=iid)
    if not login.current_user.is_active():
        flash('로그인')
        return redirect(url_for('light-cms.user_login'))
    if not i.user.is_active():
        i.user = login.current_user._get_current_object()
        i.save()
    return redirect(url_for('.image', iid=iid))


@light_cms.route('/drop/', methods=['GET', 'POST'])
def drop():
    file = request.files['file']
    i = Image()
    i.title = file.filename
    i.image = file
    uuid = shortuuid.ShortUUID().random(length=6)
    while Image.objects(iid=uuid):
        uuid = shortuuid.ShortUUID().random(length=6)
    i.iid = uuid
    if login.current_user.is_active():
        i.user = login.current_user._get_current_object()
    else:
        i.user = system_user
    i.description = ''
    i.tags = []
    i.save()
    return jsonify(id=uuid)


@light_cms.route('/g/<gid>/')
def gallery_view(gid):
    gallery = Gallery.objects.get_or_404(gid=gid)
    return render_template('gallery.html', gallery=gallery, title='앨범: %s' % gallery.title)


@light_cms.route('/g/<gid>/delete/<iid>/')
def remove_image_from_gallery(gid, iid):
    g = Gallery.objects.get_or_404(gid=gid)
    i = Image.objects.get_or_404(iid=iid)
    if g.user == i.user == login.current_user._get_current_object():
        i.gallery.remove(g)
        i.save()
        return redirect(url_for('light-cms.gallery_view', gid=gid))


@light_cms.route('/create_gallery/', methods=['GET', 'POST'])
@not_yet
def create_gallery():
    if not login.current_user.is_active():
        flash('앨범기능엔 로그인이 필요합니다')
        return redirect(url_for('light-cms.user_login'))
    if request.method == 'GET':
        return render_template('create_gallery.html', title='앨범 만들기')
    if request.method == 'POST':
        uuid = shortuuid.ShortUUID().random(length=6)
        while Gallery.objects(gid=uuid):
            uuid = shortuuid.ShortUUID().random(length=6)
        title = request.form['title']
        g = Gallery()
        g.user = login.current_user._get_current_object()
        g.gid = uuid
        g.title = title
        g.save()
        return redirect(url_for('light-cms.add_image_to_gallery', gid=g.gid))


@light_cms.route('/g/<gid>/add/')
def add_image_to_gallery(gid):
    g = Gallery.objects.get_or_404(gid=gid)
    return render_template('add_image.html', title='사진 추가', gallery=g)


@light_cms.route('/g/<gid>/drop/', methods=['GET', 'POST'])
@not_yet
def gallery_drop(gid):
    if not login.current_user.is_active():
        flash('앨범기능엔 로그인이 필요합니다')
        return redirect(url_for('light-cms.user_login'))
    g = Gallery.objects.get_or_404(gid=gid)
    file = request.files['file']
    i = Image()
    i.gallery.append(g)
    i.title = file.filename
    i.image = file
    uuid = shortuuid.ShortUUID().random(length=6)
    while Image.objects(iid=uuid):
        uuid = shortuuid.ShortUUID().random(length=6)
    i.iid = uuid
    i.user = login.current_user._get_current_object()
    i.description = ''
    i.tags = []
    i.save()
    return jsonify(id=uuid)


@login_manager.user_loader
def load_user(user_id):
    user = User.objects(id=user_id).first()
    return user


@light_cms.context_processor
def processor():
    def get_settings():
        return settings
    return {'SETTINGS': get_settings()}
