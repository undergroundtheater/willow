from flask import render_template, request, redirect, url_for, flash, Blueprint  
from flask import current_app, session 
        

from flask_security.core import current_user
from flask_security.decorators import login_required
from flask_security.decorators import roles_required
from flask.ext.classy import FlaskView, route
from werkzeug.utils import import_string
from wtforms.ext.sqlalchemy.orm import model_form

from willow.models import db, Chapter, Venue, Role
from willow.forms import NewChapterForm, NewVenueForm, NewRoleForm
from willow.forms import WLWForm

admin_blueprint = Blueprint('admin', __name__)

class BaseAdminView(FlaskView):
    decorators = [login_required]
    route_base='/'
    redirect_view = None

    @route('/')
    @route('/dashboard')
    def index(self):
        return render_template(self.get_template())

    def get_template(self,action=None):
        if action is None:
            return "admin/index.html"
        return "%s_%s.html" % (self.route_base, action)

class ModelAdminView(BaseAdminView):
    wlw_model = None
    wlw_only = []
    wlw_exclude = []
    wlw_key = None
    wlw_title = None
    wlw_children = None

    @route('/')
    def index(self):
        """ List all objects. """

        if hasattr(self, 'wlw_model') and self.wlw_model is not None:
            objects = self.wlw_model.query.filter(self.wlw_model.active == True).all()
        else:
            objects = []

        return render_template('admin/wlw_admin_index.html',
                objects=objects,
                obj_type=self.wlw_key,
                new_url=self.get_new_view_name(),
                model_title=self.wlw_title,
                secondary="")

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
            
            flash("%s (%s - ID: %s) has been updated." % (self.wlw_title, obj.name, obj.id))

        if obj is None:
            flash("Object has been deleted or does not exist.")
            return redirect(url_for(self.get_post_view_name()))


        return render_template('admin/wlw_admin_edit.html',
                form=form,
                obj_type=self.wlw_key,
                post_url=self.get_update_view_name(),
                obj=obj,
                model_title=self.wlw_title,
                children=self.wlw_children)

    def post(self):
        form = self.get_form()()
        if form.validate_on_submit():
            obj = self.wlw_model()
            form.populate_obj(obj)

            obj.active = True

            db.session.add(obj)
            db.session.commit()

            flash("%s '%s' has been created." % (self.wlw_title, obj.name))

            return redirect(url_for(self.get_redirect_view_name()))

        return render_template(self.get_template('add'), form=form)
    
    @route('/<pkid>/delete', methods=['POST'])
    def delete(self, pkid):
        obj = self.wlw_model.query.get(pkid)
        if obj:
            db.session.delete(obj)


            flash("Object deleted.")
        db.session.commit()

        return redirect(url_for(self.get_redirect_view_name()))

    def get_form(self, **kwargs):
        if self.wlw_model:
            mf = model_form(self.wlw_model,
                    base_class = self.wlw_form,
                    db_session = db.session,
                    only = self.wlw_only,
                    exclude = self.wlw_exclude,
                    field_args = kwargs)

        return mf

    def get_blueprint(self):
        return request.blueprint

    def view_base(self):
        return "%s.%s" % (self.get_blueprint(), self.__class__.__name__)

    def get_new_view_name(self):
        return "%s:new" % (self.view_base(),)

    def get_post_view_name(self):
        return "%s:post" % (self.view_base(),)

    def get_update_view_name(self):
        return "%s:edit" % (self.view_base(),)

    def get_redirect_view_name(self):
        if not self.redirect_view:
            return "%s:index" % (self.view_base(),)
        else:
            return self.redirect_view

class AdminChapterView(ModelAdminView):
    route_base="/chapter"
    wlw_model = Chapter
    wlw_only = ['name','description','venue']
    wlw_form = NewChapterForm
    wlw_key = 'chapter'
    wlw_title = 'Chapter'

class AdminVenueView(ModelAdminView):
    route_base="/venue"
    wlw_model = Venue
    wlw_only = ['name', 'description']
    wlw_form = NewVenueForm
    wlw_key = 'venue'
    wlw_title = 'Venue'
    wlw_children = 'chapters'

    @route('/<pkid>/chapters')
    def chapters(self, pkid):
        venue = self.wlw_model.query.get(pkid)
        if venue:
            return render_template('admin/wlw_admin_index.html',
                    objects=venue.chapters,
                    obj_type='chapter',
                    new_url='',
                    model_title='Chapter',
                    secondary=venue.name)

class AdminRoleView(ModelAdminView):
    route_base="/role"
    wlw_model = Role
    wlw_only = ['name', 'description', 'venue', 'chapter']
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

    def post(self):
        form = self.get_form()()
        if form.validate_on_submit():
            obj = self.wlw_model()
            form.populate_obj(obj)

            if obj.chapter and not obj.venue:
                obj.venue = obj.chapter.venue

            obj.active = True

            db.session.add(obj)
            db.session.commit()

            flash("%s '%s' has been created." % (self.wlw_title, obj.name))

            return redirect(url_for(self.get_redirect_view_name()))

        return render_template(self.get_template('add'), form=form)
    
class AdminCharacterView(ModelAdminView):
    pass

class AdminUserView(BaseAdminView):
    pass

BaseAdminView.register(admin_blueprint)
AdminChapterView.register(admin_blueprint)
AdminVenueView.register(admin_blueprint)
AdminRoleView.register(admin_blueprint)
