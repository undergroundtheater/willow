from flask import render_template, \
        redirect, \
        url_for, \
        flash, \
        current_app, \
        session

from flask_security.core import current_user
from flask_security.decorators import login_required, roles_required
from flask.ext.classy import FlaskView, route
from werkzeug.utils import import_string
from wtforms.ext.sqlalchemy.orm import model_form

from willow.models import db, Chapter, Venue, Role
from willow.forms import WLWForm, NewChapterForm, NewVenueForm, NewRoleForm

class BaseAdminView(FlaskView):
    decorators = [login_required]
    route_base="/admin"

    @route('/')
    @route('/dashboard')
    def index(self):
        return render_template(self.get_template())

    def get_template(self,action=None):
        if action is None:
            return "%s/index.html" % (self.route_base,)
        return "%s_%s.html" % (self.route_base, action)

class ModelAdminView(BaseAdminView):
    wlw_model = None
    wlw_only = []
    wlw_exclude = []
    redirect_view = 'BaseAdminView:index'
    wlw_key = None
    wlw_title = None

    @route('/')
    def index(self):
        """ List all objects. """

        objects = self.wlw_model.query.filter(self.wlw_model.active == True).all()

        return render_template('admin/wlw_admin_index.html',
                objects=objects,
                obj_type=self.wlw_key,
                new_url=self.get_new_view_name(),
                model_title=self.wlw_title)

    @route('/new')
    def new(self):
        """ Create a new object. """

        form = self.get_form()()
        return render_template('admin/wlw_admin_add.html',
                form=form,
                obj_type=self.wlw_key,
                post_url=self.get_post_view_name(),
                model_title=self.wlw_title)

    @route('/<pkid>', methods=['GET', 'POST'])
    def edit(self, pkid):
        obj = self.wlw_model.query.get(pkid)
        form = self.get_form()(obj=obj)

        if form.validate_on_submit():
            form.populate_obj(obj)
            obj.active = True # TODO - confirm this can be removed
            db.session.add(obj)
            db.session.commit()

        return render_template('admin/wlw_admin_edit.html',
                form=form,
                obj_type=self.wlw_key,
                post_url=self.get_update_view_name(),
                obj=obj,
                model_title=self.wlw_title)

    def post(self):
        form = self.get_form()()
        if form.validate_on_submit():
            obj = self.wlw_model()
            form.populate_obj(obj)

            obj.active = True

            db.session.add(obj)
            db.session.commit()

            return redirect(url_for(self.redirect_view))

        return render_template(self.get_template('add'), form=form)
    
    def delete(self, pkid):
        obj = obj.query.get(pkid)
        db.session.delete(obj)
        db.session.commit()

        return render_template(url_for(self.redirect_view))

    def get_form(self, **kwargs):
        if self.wlw_model:
            mf = model_form(self.wlw_model,
                    base_class = self.wlw_form,
                    db_session = db.session,
                    only = self.wlw_only,
                    exclude = self.wlw_exclude,
                    field_args = kwargs)

        return mf

    def get_new_view_name(self):
        return "%s:new" % (self.__class__.__name__,)

    def get_post_view_name(self):
        return "%s:post" % (self.__class__.__name__,)

    def get_update_view_name(self):
        return "%s:edit" % (self.__class__.__name__,)

class AdminChapterView(ModelAdminView):
    route_base="/admin/chapter"
    wlw_model = Chapter
    wlw_only = ['name','description','venue']
    redirect_view = 'AdminChapterView:index'
    wlw_form = NewChapterForm
    wlw_key = 'chapter'
    wlw_title = 'Chapter'

class AdminVenueView(ModelAdminView):
    route_base="/admin/venue"
    wlw_model = Venue
    wlw_only = ['name', 'description']
    redirect_view = 'AdminVenueView:index'
    wlw_form = NewVenueForm
    wlw_key = 'venue'
    wlw_title = 'Venue'

class AdminRoleView(ModelAdminView):
    route_base="/admin/role"
    wlw_model = Role
    wlw_only = ['name', 'description', 'venue', 'chapter']
    redirect_view = 'AdminRoleView:index'
    wlw_form = NewRoleForm
    wlw_key = 'role'
    wlw_title = 'Role'

    @route('/')
    def index(self):
        """ List all objects. """

        # TODO - Allow for filtering based on user
        objects = self.wlw_model.query.all()

        return render_template('admin/wlw_role_index.html',
                objects=objects,
                obj_type=self.wlw_key,
                new_url=self.get_new_view_name(),
                model_title=self.wlw_title)
    
class AdminCharacterView(ModelAdminView):
    pass

class AdminUserView(BaseAdminView):
    pass
