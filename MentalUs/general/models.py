# encoding=utf-8
from datetime import datetime
from MentalUs import db


class MTAnnouncement(db.Model):
    __tablename__ = 'mtannouncements'
    id = db.Column(db.Integer(), primary_key=True)
    publisher = db.Column(db.String(32), default='admin')
    publish_date = db.Column(db.DateTime(), default=datetime.today)
    title = db.Column(db.String(32), nullable=False)
    content = db.Column(db.Text())

    @staticmethod
    def generate_debug():
        for i in xrange(4):
            a = MTAnnouncement(title=u'还算简单话就是',
                               content=u'''01030105700604|三楼流通书库(3)29架B面6列4层''')
            db.session.add(a)
        db.session.commit()