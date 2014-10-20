import datetime
import hashlib
from flask import render_template, redirect, url_for, flash, current_app, request, session
from flask.ext.classy import FlaskView, route
from flask.ext.login import current_user, login_user, login_required
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

class AccountView(FlaskView):

    @login_required
    def index(self):
        return render_template('account/index.html')
