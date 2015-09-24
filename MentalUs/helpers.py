# encoding=utf-8


def customize_login_manager(login_manager):
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'user.login'
    login_manager.login_message = u'请在登录后再访问所有功能'
    login_manager.login_message_category = 'warning'