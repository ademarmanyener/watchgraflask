# -*- encoding: utf-8 -*-
from includes import *

def id_generator(size=24, title='', chars=string.ascii_letters + string.digits):
  current_year_without_century = time.strftime('%y')
  random_character = ''.join(random.choice(chars) for _ in range(size))
  if title == '': return str(random_character) + str(current_year_without_century)
  else: return str(title) + str(current_year_without_century) + str(random_character)

STORAGE_PATH = os.path.join(os.path.dirname(app.instance_path), 'storage')

def ID_COLUMN(size=64, nullable=False, unique=False, default=None, foreign_key=None):
    if foreign_key == None: return db.Column(db.String(size), primary_key=True, default=default)
    else: return db.Column(db.String(size), db.ForeignKey(foreign_key), nullable=nullable, unique=unique, default=default)

def STRING_COLUMN(size=64, nullable=False, unique=False, default=None): return db.Column(db.String(size), nullable=nullable, unique=unique, default=default)

def INTEGER_COLUMN(nullable=False, unique=False, default=None): return db.Column(db.Integer, nullable=nullable, unique=unique, default=default)

def BOOLEAN_COLUMN(nullable=False, unique=False, default=None): return db.Column(db.Boolean, nullable=nullable, unique=unique, default=default)

def DATE_COLUMN(nullable=False, unique=False, default=None): return db.Column(db.DateTime, nullable=nullable, unique=unique, default=default)