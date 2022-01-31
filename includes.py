# -*- encoding: utf-8 -*-
from datetime import date, time, datetime
import pytz
import time
import random, string
from random import randint
import sys
import re
from math import ceil
# PASSLIB HASH
from passlib.hash import sha512_crypt
# FLASK
from flask import Flask, render_template, redirect, request, url_for, session, flash, g, json, jsonify, make_response, send_from_directory, send_file
from flask_jsglue import JSGlue
from werkzeug.utils import secure_filename
# FLASK MAIL
from flask_mail import Mail, Message
# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, desc, asc, case
#from sqlalchemy_serializer import SerializerMixin
# FLASK MIGRATE
from flask_migrate import Migrate
# CSRF PROTECTION
from flask_wtf.csrf import CSRFProtect
# FLASK FORMS
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Email
# SECRET KEY
import os
SECRET_KEY = os.urandom(32)
# TMDBSIMPLE
import tmdbsimple as tmdb
# babel for some useful shits
from babel.dates import format_date, format_datetime, format_time
# slugify
from slugify import slugify

from settings import SETTINGS # CONFIG FILE

#PY_TIMEZONE = 'Europe/Istanbul'
PY_TIMEZONE = SETTINGS['timezone']

tmdb.API_KEY = SETTINGS['tmdb']['api_key']
TMDB_LANGUAGE = SETTINGS['tmdb']['language']

app = Flask(__name__)
#app.url_map.strict_slashes = False # NOT RECOMMENDED
app.config['SECRET_KEY'] = os.urandom(32)
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = SETTINGS['recaptcha']['public_key']
app.config['RECAPTCHA_PRIVATE_KEY'] = SETTINGS['recaptcha']['private_key']

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = SETTINGS['email']['username']
app.config['MAIL_PASSWORD'] = SETTINGS['email']['password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS['app_config']['sqlalchemy_database_uri']

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size' : 100, 'pool_recycle' : 280}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
db.init_app(app) # re-initing the db, it's stupid but works i guess

migrate = Migrate(app, db, render_as_batch=True)

# 3 hr = 10,800 sec
# 10 hr = 36,000 sec
app.config['WTF_CSRF_TIME_LIMIT'] = 36000
csrf = CSRFProtect()
csrf.init_app(app)

jsglue = JSGlue()
jsglue.init_app(app)

current_time = time.strftime('%Y-%m-%d %H:%M:%S')

from run_app import *
from forms import *

# MISCELLANEOUS BEGIN
from miscellaneous.restricted_usernames import is_restricted
from miscellaneous.hash import hash_str_hash, hash_str_verify
from miscellaneous.soup import Soup_Local, Soup_Local_2, Soup_Global, soup_global_beta
# MISCELLANEOUS END

from database_modules.variable import *
from database_modules.collection import *
from database_modules.player import *
from database_modules.genre import *
from database_modules.language import *
from database_modules.country import *
from database_modules.cast import *
from database_modules.content import *
from database_modules.account import *
from database_modules.report import *

#from functions.generator import * # IT'S NOT USED. SO IT'S DEPRECATED
from functions.check import *
from functions.authentication import *
from functions.tmdbsimpleasy import *
from functions.other import *
from functions.jinja import *
from functions._init import *
from functions.upload_image_resize import *

from functions.ajax.main import *
from functions.ajax.profile import *
from functions.ajax.admin import *

from routes import test, server_error_handlers, home, search, contact, signin, signup, accountprofile, welcome, whoiswatching, settings, content_handlers, movie, tv, interstitial, catalog, collection_handlers, report, cast_handlers, message_handlers
from routes.adminpanel import home, highlights, contents, accounts, profiles, casts, collections, comments
from routes.adminpanel_v2 import home, list, edit, function
