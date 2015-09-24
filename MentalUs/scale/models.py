# encoding=utf-8
import base64
from datetime import datetime
from flask import json
from MentalUs import db, logger


class MTScale(db.Model):
    __tablename__ = 'mtscales'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    scale_introductions = db.Column(db.Text())
    scale_content = db.Column(db.PickleType())
    scale_algorithm = db.Column(db.PickleType())

    @property
    def scale_json(self):
        return json.dumps(self.scale_content)

    @staticmethod
    def generate_debug():
        from scale_files import upi
        for i in xrange(1):
            s = MTScale(title=upi.scale_title, scale_introductions=upi.scale_introductions,
                        scale_content=upi.scale_content, scale_algorithm=upi.calc_scale)
            db.session.add(s)
        db.session.commit()


class MTUnfinishedScale(db.Model):
    __tablename__ = 'mtunfinishedscales'
    id = db.Column(db.Integer(), primary_key=True)
    setup_time = db.Column(db.DateTime(), default=datetime.today)
    end_time = db.Column(db.DateTime(), default=datetime.today)
    started = db.Column(db.Boolean(), default=False)
    answer_content = db.Column(db.Text(), default=json.dumps(dict()))
    user_id = db.Column(db.Integer())
    scale_id = db.Column(db.Integer())

    @property
    def scale(self):
        scale = MTScale.query.filter_by(id=self.scale_id).first()
        return scale

    @property
    def answers(self):
        return json.loads(self.answer_content)

    def add_answer(self, question_id, answer):
        answer_dict = self.answers
        answer_dict[question_id] = answer
        self.answer_content = json.dumps(answer_dict)

    @staticmethod
    def generate_debug():
        pass
        # for i in xrange(3000):
        #     us = MTUnfinishedScale(user_id=i, scale_id=i + 1)
        #     db.session.add(us)
        # for i in xrange(1500):
        #     us = MTUnfinishedScale(user_id=i, scale_id=i + 1, started=True)
        #     db.session.add(us)
        # db.session.commit()


class MTScaleResult(db.Model):
    __tablename__ = 'mtscaleresults'
    id = db.Column(db.Integer, primary_key=True)
    setup_time = db.Column(db.DateTime(), default=datetime.today)
    finished_time = db.Column(db.DateTime(), default=datetime.today)
    result_content = db.Column(db.Text(), default=json.dumps(dict()))
    result_score = db.Column(db.Text(), default=json.dumps(dict()))
    user_id = db.Column(db.Integer())
    scale_id = db.Column(db.Integer())

    @property
    def title(self):
        scale = MTScale.query.filter_by(id=self.scale_id).first()
        if scale is None:
            logger.error('Not found scale id = %d' % self.scale_id)
            return ''
        return scale.title

    @property
    def consuming(self):
        return int((self.finished_time - self.setup_time).total_seconds() / 60)

    @staticmethod
    def generate_debug():
        pass
        # for i in xrange(1000):
        #     us = MTScaleResult(user_id=i, scale_id=i + 1)
        #     db.session.add(us)
        # db.session.commit()
