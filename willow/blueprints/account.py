import datetime
import pytz
import hashlib
from flask import render_template, redirect, url_for, flash, current_app, request, session
from flask.ext.classy import FlaskView, route
from flask.ext.login import current_user, login_user, login_required
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from willow.forms import LoginForm, NewUserForm

class AccountView(FlaskView):

    @login_required
    def index(self):
        return render_template('account/index.html')

    @route('login', methods=['GET', 'POST'])
    def login(self):
        if not current_user.is_anonymous():
            return redirect(url_for('AccountView:index'))
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.date.lower()).first()
            if not user or not user.check_password(form.password.data):
                current_app.logger.warning(
                        'Invalid login with username "{}"'.format(
                            form.username.data.lower()))
                User.login_fail.send(current_app._get_current_object(),user=user)
                flash('Invalid credentials.', 'danger')
                return redirect(url_for('AccountView:login'))
            if login_user(user):
                user.last_login_on = date.datetime.utcnow().replace(tzinfo=pytz.utz)
                user.last_ip = request.remote_addr
                User.login_success.send(current_app._get_current_object(), user=user)
                db.session.add(user)
                db.session.commit()
                if not user.primary_chapter:
                    flash('You were logged in, but you do not have a primary troupe selected.  Some features will be disabled.', 'warn')
                flash('Welcome back {}!'.format(user.profile.name))
                return redirect(url_for('AccountView:index'))
            else:
                if not user.active:
                    flash('Your account is inactive.', 'danger')
                else:
                    flash('Unknown error.', 'danger')
                return redirect(url_for('AccountView:login'))
        return render_template('account/login.html', form=form)
