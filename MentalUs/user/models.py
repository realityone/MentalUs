# encoding=utf-8
from datetime import datetime
from flask import json
from wtforms import StringField, SelectField
from werkzeug.security import generate_password_hash, check_password_hash
from MentalUs.scale.models import MTScale, MTScaleResult, MTUnfinishedScale
from MentalUs import db, login_manager, logger


class MTUser(db.Model):
    __tablename__ = 'mtusers'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(32))
    sex = db.Column(db.String(16))
    nation = db.Column(db.String(16))
    birthday = db.Column(db.Date())
    email = db.Column(db.String(64))
    phone = db.Column(db.String(32))
    blood_type = db.Column(db.String(16))
    health = db.Column(db.String(64))
    commit = db.Column(db.Text())
    registration_date = db.Column(db.DateTime(), default=datetime.today)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def succeed_scales(self):
        scales = MTScaleResult.query.filter_by(user_id=self.id)
        return scales

    @property
    def notstart_scales(self):
        scales = MTUnfinishedScale.query.filter_by(user_id=self.id, started=False)
        return scales

    @property
    def working_scales(self):
        scales = MTUnfinishedScale.query.filter_by(user_id=self.id, started=True)
        return scales

    @property
    def extend(self):
        extend = MTUserExtendInfo.query.filter_by(user_id=self.id).first()
        if extend is None:
            extend = MTUserExtendInfo(user_id=self.id)
            db.session.add(extend)
            db.session.commit()
        return extend

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return MTUser.query.get(int(user_id))

    @staticmethod
    def generate_debug():
        for i in xrange(1):
            u = MTUser(username='120603118', password='123456')
            db.session.add(u)
        db.session.commit()


class MTUserExtendInfo(db.Model):
    __tablename__ = 'mtuserextendinfos'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    extend_json = db.Column(db.Text(), default=json.dumps(dict()))

    @property
    def extend_info(self):
        return json.loads(self.extend_json)

    @extend_info.setter
    def extend_info(self, extend_info):
        self.extend_json = json.dumps(extend_info)


class MTExtendFields(db.Model):
    """
    :param details expample
    '{"title":"\u5b66\u9662", "type": "string"}'
    or
    '{"title":"\u73ed\u7ea7", "type": "select", "choices": [[1, 1], [2, 2]]}'
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    details = db.Column(db.Text(), default=json.dumps(dict()))

    def generate_wtfield(self):
        try:
            details = json.loads(self.details)
            if details.get('type', 'string') == 'select':
                field = SelectField(details['title'],
                                    choices=[(str(value), str(label)) for value, label in details['choices']])
            else:
                field = StringField(details['title'])
            return dict(name=self.name, item=field)
        except ValueError:
            logger.error('extend field %s generate error' % self.name)
            return False

    @staticmethod
    def generate_debug():
        fd = [{'title': u'学院'}, {'title': u'专业'}, {'title': u'选择', 'type': 'select', 'choices': [[1, 1], [2, 2]]}]
        fa = MTExtendFields(name='collage', details=json.dumps(fd[0]))
        fb = MTExtendFields(name='major', details=json.dumps(fd[1]))
        fc = MTExtendFields(name='choice', details=json.dumps(fd[2]))
        db.session.add_all([fa, fb, fc])
        db.session.commit()


