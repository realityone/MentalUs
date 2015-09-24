# encoding=utf-8
from flask import session, redirect, url_for, \
    flash, render_template, request
from flask.ext.login import login_user, logout_user, \
    login_required, current_user
from MentalUs import logger
from MentalUs.general.views import MTBaseView
from models import MTUser, MTExtendFields, db
from forms import MTUserLoginForm, MTUserPwdForm, MTUserBaseProfileForm
from . import user


class MTUserLoginView(MTBaseView):
    template = 'user/login.html'

    def get(self, *args, **kwargs):
        form = MTUserLoginForm()
        form.username.data = session.pop('username', '')
        self.content['form'] = form
        return render_template(self.template, **self.content)

    def post(self, *args, **kwargs):
        form = MTUserLoginForm()
        if form.validate_on_submit():
            this_user = MTUser.query.filter_by(username=form.username.data).first()
            if this_user is not None and this_user.verify_password(form.password.data):
                login_user(this_user, False)
                return redirect(request.args.get('next') or url_for('general.index'))
        flash(u'认证失败，请检查输入的用户名和密码', category='danger')
        session['username'] = form.username.data
        self.content['form'] = form
        return render_template(self.template, **self.content)


class MTUserPwdView(MTBaseView):
    template = 'user/password.html'
    decorators = [login_required]

    def get(self, *args, **kwargs):
        form = MTUserPwdForm()
        self.content['form'] = form
        return render_template(self.template, **self.content)

    def post(self, *args, **kwargs):
        form = MTUserPwdForm()
        if form.validate_on_submit() and current_user.verify_password(form.old_pwd.data):
            current_user.password = form.new_pwd.data
            db.session.add(current_user)
            flash(u'密码修改成功', 'success')
        else:
            flash(u'密码修改失败，请检查后再试', 'danger')
        return redirect(url_for('user.password'))


class MTUserProfileView(MTBaseView):
    template = 'user/profile.html'
    decorators = [login_required]

    def __init__(self):
        super(MTUserProfileView, self).__init__()
        extend_list = MTExtendFields.query.all()

        for extend in extend_list:
            extend_field = extend.generate_wtfield()
            MTUserBaseProfileForm.add_extend(extend_field['name'], extend_field['item'])
        self.form = MTUserBaseProfileForm()

    def get(self, *args, **kwargs):
        for item in self.form.bases:
            self.form[item].data = getattr(current_user, item, '')

        try:
            extends_data = current_user.extend.extend_info
            for item in extends_data:
                self.form[item].data = extends_data[item]
        except Exception, e:
            logger.warning(e)

        self.content['form'] = self.form
        return render_template(self.template, **self.content)

    def post(self, *args, **kwargs):
        if self.form.validate_on_submit():
            for item in self.form.bases:
                setattr(current_user, item, self.form[item].data)
            extends_data = dict()
            for item in self.form.extends:
                extends_data[item] = self.form[item].data
            current_user.extend.extend_info = extends_data
            db.session.add(current_user)
            flash(u'个人资料修改成功', 'success')
        else:
            flash(u'资料填写有误', 'danger')
        return redirect(url_for('user.profile'))


user.add_url_rule('/login', view_func=MTUserLoginView.as_view('login'))
user.add_url_rule('/password', view_func=MTUserPwdView.as_view('password'))
user.add_url_rule('/profile', view_func=MTUserProfileView.as_view('profile'))


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))