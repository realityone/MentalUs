# encoding=utf-8
import base64
from flask import render_template, json, request, jsonify, redirect, url_for
from flask.ext.login import current_user, login_required
from MentalUs.general.views import MTBaseView
from models import MTScale, MTScaleResult, MTUnfinishedScale, db
from . import scale


class MTSucceedScaleView(MTBaseView):
    template = 'scale/succeed.html'
    decorators = [login_required]

    def get(self, *args, **kwargs):
        page = request.args.get('page', 1, type=int)
        succeed_scales_pagination = current_user.succeed_scales.order_by(MTScaleResult.finished_time.desc()).paginate(
            page, per_page=15, error_out=False
        )
        self.content['succeed_scales_pagination'] = succeed_scales_pagination
        return render_template(self.template, **self.content)


class MTUnfinishedScaleView(MTBaseView):
    template = 'scale/notfinished.html'
    decorators = [login_required]

    def get(self, *args, **kwargs):
        page = request.args.get('page', 1, type=int)
        working_scales = current_user.working_scales.all()
        notstart_scales_pagination = current_user.notstart_scales.order_by(
            MTUnfinishedScale.setup_time.desc()).paginate(
            page, per_page=15, error_out=False
        )
        self.content['working_scale_list'] = working_scales
        self.content['notstart_scales_pagination'] = notstart_scales_pagination
        return render_template(self.template, **self.content)


class MTApplyScaleView(MTBaseView):
    template = 'scale/apply.html'
    decorators = [login_required]

    def get(self, *args, **kwargs):
        page = request.args.get('page', 1, type=int)
        scale_pagination = MTScale.query.order_by(MTScale.id.asc()).paginate(
            page, per_page=30, error_out=False
        )
        self.content['scale_pagination'] = scale_pagination
        return render_template(self.template, **self.content)

    def post(self, *args, **kwargs):
        scale_id = request.form.get('scale', None, type=int)
        applyed = MTUnfinishedScale.query.filter_by(user_id=current_user.id, scale_id=scale_id).first()
        result = {'result': u'申请测试失败'}
        if applyed is not None:
            result['result'] = u'已经申请了此测试'
        elif scale_id is not None:
            scale_task = MTUnfinishedScale(user_id=current_user.id, scale_id=scale_id)
            db.session.add(scale_task)
            result['result'] = u'申请测试成功'
        return jsonify(result)

    @staticmethod
    @scale.route('/apply/<int:scale_id>')
    @login_required
    def introduction_scale(scale_id):
        this_scale = MTScale.query.get_or_404(scale_id)
        return jsonify(title=this_scale.title, introduction=this_scale.scale_introductions)


class MTScaleAnswerView(MTBaseView):
    template = 'scale/answer.html'
    decorators = [login_required]

    @staticmethod
    def have_task(scale_id):
        permit_scale = MTUnfinishedScale.query.filter_by(user_id=current_user.id, scale_id=scale_id).first()
        return permit_scale

    def get(self, scale_id, *args, **kwargs):
        task = self.have_task(scale_id)
        if task is None:
            return redirect(url_for('general.index'))
        self.content['task'] = task
        self.content['scale'] = task.scale
        return render_template(self.template, **self.content)

    def post(self, scale_id, *args, **kwargs):
        question_id = request.form.get('q', None, type=int)
        answer = request.form.get('a', None, type=int)
        result = {'result': 0}
        if question_id is not None or answer is not None:
            task = MTUnfinishedScale.query.filter_by(user_id=current_user.id, scale_id=scale_id).first()
            if task is not None:
                task.add_answer(question_id, answer)
                print task.answer_content
                result['result'] = 1
        return jsonify(result)

    @staticmethod
    @scale.route('/scale/<int:scale_id>')
    @login_required
    def scale_content(scale_id):
        this_scale = MTScale.query.get_or_404(scale_id)
        return json.dumps(this_scale.scale_content)


scale.add_url_rule('/succeed', view_func=MTSucceedScaleView.as_view('succeed'))
scale.add_url_rule('/unfinished', view_func=MTUnfinishedScaleView.as_view('unfinished'))
scale.add_url_rule('/apply', view_func=MTApplyScaleView.as_view('apply'))
scale.add_url_rule('/answer/<int:scale_id>', view_func=MTScaleAnswerView.as_view('answer'))
