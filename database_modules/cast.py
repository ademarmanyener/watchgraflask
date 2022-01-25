# -*- encoding: utf-8 -*-
from includes import *

"""
gender
======
0 - not specified
1 - female
2 - male 
3 - non-binary 
"""
class cast(db.Model):
  __tablename__ = 'cast'
  idCast = ID_COLUMN(default=str(id_generator(title='cast_', size=32)))
  idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
  idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
  gender = INTEGER_COLUMN() # 0, 1, 2, 3
  name = STRING_COLUMN()
  nameUrl = STRING_COLUMN()
  biography = STRING_COLUMN(size=2048)
  idTmdb = STRING_COLUMN(nullable=True)
  idImdb = STRING_COLUMN(nullable=True)
  idTwitter = STRING_COLUMN(nullable=True)
  idInstagram = STRING_COLUMN(nullable=True)
  imagePoster = STRING_COLUMN(size=2048, nullable=True)
  adult = INTEGER_COLUMN(default=0)
  visibility = INTEGER_COLUMN(default=1)
  birthPlace = STRING_COLUMN(nullable=True, size=512)
  birthDate = STRING_COLUMN(nullable=True)
  deathDate = STRING_COLUMN(nullable=True)
  lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
  addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
  def __init__(self, idAddProfile, idAddAccount, gender, name, nameUrl, biography, idTmdb, idImdb, idTwitter, idInstagram, imagePoster, adult, visibility, birthPlace, birthDate, deathDate, lastEditDate):
    self.idCast = str(id_generator(title='cast_', size=32))
    self.idAddProfile = idAddProfile
    self.idAddAccount = idAddAccount
    self.gender = gender
    self.name = name
    self.nameUrl = nameUrl
    self.biography = biography
    self.idTmdb = idTmdb
    self.idImdb = idImdb
    self.idTwitter = idTwitter
    self.idInstagram = idInstagram
    self.imagePoster = imagePoster
    self.adult = adult
    self.visibility = visibility
    self.birthPlace = birthPlace
    self.birthDate = birthDate
    self.deathDate = deathDate
    self.lastEditDate = lastEditDate
    self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    #### FOLDER
    cast_dir = os.path.join(STORAGE_PATH, 'cast', self.idCast)
    # mkdir: /storage/cast/{{idCast}}
    if not os.path.exists(cast_dir): os.makedirs(cast_dir)
    """
    # mkdir: /storage/cast/{{idCast}}/poster/{{imagePoster}}
    if not os.path.exists(os.path.join(cast_dir, 'poster')): os.makedirs(os.path.join(cast_dir, 'poster'))
    """
    #### END FOLDER

  def drop(self):
    #### FOLDER
    cast_dir = os.path.join(STORAGE_PATH, 'cast', self.idCast)
    os.system('rm -rf ' + cast_dir)
    #### END FOLDER

    for get_content_cast in contentCast.query.filter_by(idCast=self.idCast).all():
      get_content_cast.drop()

    for get_cast_comment in castComment.query.filter_by(idCast=self.idCast).all():
      get_cast_comment.drop()

    db.session.delete(self)
    db.session.commit()

class contentCast(db.Model):
  __tablename__ = 'contentcast'
  idContentCast = ID_COLUMN(default=str(id_generator(title='content_cast_', size=32)))
  idContent = ID_COLUMN(foreign_key='content.idContent')
  idCast = ID_COLUMN(foreign_key='cast.idCast')
  character = STRING_COLUMN()
  order = INTEGER_COLUMN(default=1)
  def __init__(self, idContent, idCast, character, order):
    self.idContentCast = default=str(id_generator(title='content_cast_', size=32))
    self.idContent = idContent
    self.idCast = idCast
    self.character = character
    self.order = order

  def drop(self):
    db.session.delete(self)
    db.session.commit()

class castComment(db.Model):
    __tablename__ = 'castcomment'
    idComment = ID_COLUMN(default=str(id_generator(title='cast_comment_', size=32)))
    idCast = ID_COLUMN(foreign_key='cast.idCast')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    text = STRING_COLUMN(size=512)
    replyTo = STRING_COLUMN(nullable=True)
    visibility = INTEGER_COLUMN(default=1)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idCast, idAddProfile, idAddAccount, text, replyTo, visibility, lastEditDate):
        self.idComment = str(id_generator(title='cast_comment_', size=32))
        self.idCast = idCast 
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.text = text
        self.replyTo = replyTo
        self.visibility = visibility
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        for get_cast_comment_rate in castCommentRate.query.filter_by(idComment=self.idComment).all():
            get_cast_comment_rate.drop()

        for get_cast_comment_replyto in castComment.query.filter_by(replyTo=self.idComment).all():
            get_cast_comment_replyto.drop()

        db.session.delete(self)
        db.session.commit()

class castCommentRate(db.Model):
    __tablename__ = 'castcommentrate'
    idRate = ID_COLUMN(default=str(id_generator(title='cast_comment_rate_', size=32)))
    idCast = ID_COLUMN(foreign_key='cast.idCast')
    idComment = ID_COLUMN(foreign_key='castcomment.idComment')
    idRateProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idRateAccount = ID_COLUMN(foreign_key='account.idAccount')
    rateType = STRING_COLUMN(default='LIKE')
    rateDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idCast, idComment, idRateProfile, idRateAccount, rateType):
      self.idRate = str(id_generator(title='cast_comment_rate_', size=32))
      self.idCast = idCast
      self.idComment = idComment 
      self.idRateProfile = idRateProfile 
      self.idRateAccount = idRateAccount 
      self.rateType = rateType 
      self.rateDate = datetime.now(pytz.timezone(PY_TIMEZONE)) 

    def drop(self):
        db.session.delete(self)
        db.session.commit()
