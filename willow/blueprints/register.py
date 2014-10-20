from flask import render_template, flash, current_app, redirect, url_for, session, request
from flask.ext.classy import FlaskView, route
from slugify import slugify
from willow.forms import NewUserForm, ProfileForm
from willow.models import User, Profile, db

class RegisterView(FlaskView):

    @route('index', methods=['GET', 'POST'])
    def index(self):
        form = NewUserForm()
        if form.validate_on_submit():
            user = User(
                        username = form.username.data,
                        email = form.email.data
                    )
            user.update_password(form.password.data)
            db.session.add(user)
            
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.exception(e)
                db.session.rollback()
            else:
                User.new_user.send(current_app._get_current_object(), model=user, password=form.password.data)
                session['user_id'] = user.id

            return redirect(url_for('RegisterView:profile'))
        
        return render_template('register/index.html', form=form)

    @route('profile', methods=['GET', 'POST'])
    def profile(self):
        user = User.query.get(int(session['user_id']))
        if user.profile:
            return redirect(url_for('AccountView:login'))

        form = ProfileForm()
        if form.validate_on_submit():
            profile = Profile(
                        name = form.name.data,
                        user_id = user.id,
                        active = True,
                        admin = False
                    )
            db.session.add(profile)
            user.profile = profile
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('AccountView:index'))
        return render_template('register/profile.html', form=form)

