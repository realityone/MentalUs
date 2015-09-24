# encoding=utf-8
from flask import render_template, current_app, request, jsonify
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from models import MTAnnouncement
from . import general


class MTBaseView(MethodView):
    template = 'general/base.html'
    content = dict()

    def __init__(self):
        self.content['title'] = current_app.config.get('MENTALUS_TITLE', 'MentalUs')
        super(MTBaseView, self).__init__()

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class MTIndexView(MTBaseView):
    template = 'general/index.html'
    decorators = [login_required]

    def get(self, *args, **kwargs):
        announcement_list = MTAnnouncement.query.order_by(MTAnnouncement.publish_date.desc()).limit(4)
        succeed_list = current_user.succeed_scales.limit(4).all()
        working_list = current_user.working_scales.limit(4).all()
        notstart_list = current_user.notstart_scales.limit(4).all()
        self.content['announcement_list'] = announcement_list
        self.content['working_list'] = working_list
        self.content['notstart_list'] = notstart_list
        self.content['succeed_list'] = succeed_list
        return render_template(self.template, **self.content)


class MTAnnouncementView(MTBaseView):
    template = 'general/announcement.html'
    decorators = [login_required]

    def get(self, *args, **kwargs):
        page = request.args.get('page', 1, type=int)
        pagination = MTAnnouncement.query.order_by(MTAnnouncement.publish_date.desc()).paginate(
            page, per_page=15, error_out=False
        )
        self.content['announcement_pagination'] = pagination
        return render_template(self.template, **self.content)

    @staticmethod
    @general.route('/announcement/<int:announcement_id>')
    @login_required
    def announcement_details(announcement_id):
        announcement = MTAnnouncement.query.get_or_404(announcement_id)
        return jsonify(dict(title=announcement.title, content=announcement.content))


general.add_url_rule('/', view_func=MTIndexView.as_view('index'))
general.add_url_rule('/announcement', view_func=MTAnnouncementView.as_view('announcement'))