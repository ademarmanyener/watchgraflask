# -*- encoding: utf-8 -*-
from includes import *

class account(db.Model):
    __tablename__ = 'account'
    idAccount = ID_COLUMN(default=str(id_generator(title='account_', size=32)))
    username = STRING_COLUMN(unique=True)
    password = STRING_COLUMN(size=512)
    securityPassword = STRING_COLUMN(size=512, nullable=True)
    emailAddress = STRING_COLUMN(unique=True)
    permission = STRING_COLUMN(default='USER') # it can be 'USER', 'SYSTEM'
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    signupDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, username, password, securityPassword, emailAddress, permission, lastEditDate):
        self.idAccount = str(id_generator(title='account_', size=32))
        self.username = username
        self.password = password
        self.securityPassword = securityPassword
        self.emailAddress = emailAddress
        self.permission = permission
        self.lastEditDate = lastEditDate
        self.signupDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        for get_reference in reference.query.filter(or_(reference.idGuestAccount == self.idAccount, reference.idHostAccount == self.idAccount)).all():
            get_reference.drop()

        for get_profile in profile.query.filter_by(idAccount=self.idAccount).all():
            get_profile.drop()

        for get_password_recovery in accountPasswordRecovery.query.filter_by(idAccount=self.idAccount).all():
            get_password_recovery.drop()

        db.session.delete(self)
        db.session.commit()

class accountPasswordRecovery(db.Model):
  __tablename__ = 'accountpasswordrecovery'
  idRecovery = ID_COLUMN(default=str(id_generator(title='recovery_', size=32)))
  idAccount = ID_COLUMN(foreign_key='account.idAccount')
  generatedKey = STRING_COLUMN(size=512)
  recoveryRequestDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
  def __init__(self, idAccount):
    self.idRecovery = str(id_generator(title='recovery_', size=32))
    self.idAccount = idAccount
    self.generatedKey = str(id_generator(size=256))
    self.recoveryRequestDate = datetime.now(pytz.timezone(PY_TIMEZONE))

  def drop(self):
    db.session.delete(self)
    db.session.commit()

class profile(db.Model):
    __tablename__ = 'profile'
    idProfile = ID_COLUMN(default=str(id_generator(title='profile_', size=32)))
    idAccount = ID_COLUMN(foreign_key='account.idAccount')
    username = STRING_COLUMN()
    password = STRING_COLUMN(nullable=True)
    biography = STRING_COLUMN(nullable=True)
    adult = INTEGER_COLUMN(default=1)
    permission = STRING_COLUMN(default='USER') # it can be 'USER', 'EDITOR', 'ADMIN'
    private = INTEGER_COLUMN(default=0)
    imageAvatar = STRING_COLUMN(size=2048)
    imageBackground = STRING_COLUMN(size=2048)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idAccount, username, password, biography, adult, permission, private, imageAvatar, imageBackground, lastEditDate):
        self.idProfile = str(id_generator(title='profile_', size=32))
        self.idAccount = idAccount
        self.username = username
        self.password = password
        self.biography = biography
        self.adult = adult
        self.permission = permission
        self.private = private
        self.imageAvatar = imageAvatar
        self.imageBackground = imageBackground
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

        #### FOLDER
        profile_dir = os.path.join(STORAGE_PATH, 'profile', self.idProfile)

        avatars_list_dir = os.path.join(os.path.dirname(app.instance_path), 'static', 'img', 'avatars')
        backgrounds_list_dir = os.path.join(os.path.dirname(app.instance_path), 'static', 'img', 'backgrounds')

        # mkdir: /storage/profile/{{idProfile}}
        if not os.path.exists(profile_dir): os.makedirs(profile_dir)
        #### END FOLDER

    def drop(self):
        #### FOLDER
        profile_dir = os.path.join(STORAGE_PATH, 'profile', self.idProfile)
        os.system('rm -rf ' + profile_dir)
        #### END FOLDER

        for get_follow in follow.query.filter(or_(follow.idFollowerProfile == self.idProfile, follow.idFollowingProfile == self.idProfile)).all():
            get_follow.drop()

        for get_collection in collection.query.filter_by(idAddProfile=self.idProfile).all():
            get_collection.drop()

        for get_movie_comment in movieComment.query.filter_by(idAddProfile=self.idProfile).all():
            get_movie_comment.drop()

        for get_movie_comment_rate in movieCommentRate.query.filter_by(idRateProfile=self.idProfile).all():
            get_movie_comment_rate.drop()

        for get_tv_comment in tvComment.query.filter_by(idAddProfile=self.idProfile).all():
            get_tv_comment.drop()

        for get_tv_comment_rate in tvCommentRate.query.filter_by(idRateProfile=self.idProfile).all():
            get_tv_comment_rate.drop()

        for get_tv_title_comment in tvTitleComment.query.filter_by(idAddProfile=self.idProfile).all():
            get_tv_title_comment.drop()

        for get_tv_title_comment_rate in tvTitleCommentRate.query.filter_by(idRateProfile=self.idProfile).all():
            get_tv_title_comment_rate.drop()

        for get_cast_comment in castComment.query.filter_by(idAddProfile=self.idProfile).all():
            get_cast_comment.drop()

        for get_cast_comment_rate in castCommentRate.query.filter_by(idRateProfile=self.idProfile).all():
            get_cast_comment_rate.drop()

        # for get_recommendation_algorithm_movie_content in recommendationAlgorithmMovieContent.query.filter_by(idProfile=self.idProfile).all():
            # get_recommendation_algorithm_movie_content.drop()

        # for get_recommendation_algorithm_tv_content in recommendationAlgorithmTVContent.query.filter_by(idProfile=self.idProfile).all():
            # get_recommendation_algorithm_tv_content.drop()

        for get_latest_watched_episode in latestWatchedEpisode.query.filter_by(idAddProfile=self.idProfile).all():
            get_latest_watched_episode.drop()

        # transfer to docker profile
        for get_movie_player in moviePlayer.query.filter_by(idAddProfile=self.idProfile).all():
            get_movie_player.idAddAccount = account.query.filter_by(idAccount=profile.query.filter_by(permission='DOCKER').first().idAccount).first().idAccount
            get_movie_player.idAddProfile = profile.query.filter_by(permission='DOCKER').first().idProfile

        for get_tv_player in tvPlayer.query.filter_by(idAddProfile=self.idProfile).all():
            get_tv_player.idAddAccount = account.query.filter_by(idAccount=profile.query.filter_by(permission='DOCKER').first().idAccount).first().idAccount
            get_tv_player.idAddProfile = profile.query.filter_by(permission='DOCKER').first().idProfile

        for get_tv_episode_content in tvEpisodeContent.query.filter_by(idAddProfile=self.idProfile).all():
            get_tv_episode_content.idAddAccount = account.query.filter_by(idAccount=profile.query.filter_by(permission='DOCKER').first().idAccount).first().idAccount
            get_tv_episode_content.idAddProfile = profile.query.filter_by(permission='DOCKER').first().idProfile

        for get_tv_season_content in tvSeasonContent.query.filter_by(idAddProfile=self.idProfile).all():
            get_tv_season_content.idAddAccount = account.query.filter_by(idAccount=profile.query.filter_by(permission='DOCKER').first().idAccount).first().idAccount
            get_tv_season_content.idAddProfile = profile.query.filter_by(permission='DOCKER').first().idProfile

        for get_highlight_content in highlightContent.query.filter_by(idAddProfile=self.idProfile).all():
            get_highlight_content.idAddAccount = account.query.filter_by(idAccount=profile.query.filter_by(permission='DOCKER').first().idAccount).first().idAccount
            get_highlight_content.idAddProfile = profile.query.filter_by(permission='DOCKER').first().idProfile

        for get_content in content.query.filter_by(idAddProfile=self.idProfile).all():
            get_content.idAddAccount = account.query.filter_by(idAccount=profile.query.filter_by(permission='DOCKER').first().idAccount).first().idAccount
            get_content.idAddProfile = profile.query.filter_by(permission='DOCKER').first().idProfile

        for get_cast in cast.query.filter_by(idAddProfile=self.idProfile).all():
            get_cast.idAddAccount = account.query.filter_by(idAccount=profile.query.filter_by(permission='DOCKER').first().idAccount).first().idAccount
            get_cast.idAddProfile = profile.query.filter_by(permission='DOCKER').first().idProfile

        db.session.delete(self)
        db.session.commit()

class reference(db.Model):
    __tablename__ = 'reference'
    idReference = ID_COLUMN(default=str(id_generator(title='reference_', size=32)))
    idGuestAccount = ID_COLUMN(foreign_key='account.idAccount')
    idHostAccount = ID_COLUMN(foreign_key='account.idAccount')
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idGuestAccount, idHostAccount):
        self.idReference = str(id_generator(title='reference_', size=32))
        self.idGuestAccount = idGuestAccount
        self.idHostAccount = idHostAccount
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class follow(db.Model):
    __tablename__ = 'follow'
    idFollow = ID_COLUMN(default=str(id_generator(title='follow_', size=32)))
    idFollowerProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idFollowerAccount = ID_COLUMN(foreign_key='account.idAccount')
    idFollowingProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idFollowingAccount = ID_COLUMN(foreign_key='account.idAccount')
    followDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idFollowerProfile, idFollowerAccount, idFollowingProfile, idFollowingAccount):
        self.idFollow = str(id_generator(title='follow_', size=32))
        self.idFollowerProfile = idFollowerProfile
        self.idFollowerAccount = idFollowerAccount
        self.idFollowingProfile = idFollowingProfile
        self.idFollowingAccount = idFollowingAccount
        self.followDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

"""
# BETA!
class recommendationAlgorithmMovieContent(db.Model):
    __tablename__ = 'recommendationalgorithmmoviecontent'
    idAlgorithm = ID_COLUMN(default=str(id_generator(title='recomendation_algorithm_movie_content_', size=16)))
    idAccount = ID_COLUMN(foreign_key='account.idAccount')
    idProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idGenre = ID_COLUMN(foreign_key='moviegenrelist.idGenre')
    genreType = STRING_COLUMN() # 'MOVIE' or 'TV'
    genreValue = INTEGER_COLUMN()
    def __init__(self, idAccount, idProfile, idGenre, genreType, genreValue):
        self.idAlgorithm = str(id_generator(title='recomendation_algorithm_movie_content_', size=16))
        self.idAccount = idAccount
        self.idProfile = idProfile
        self.idGenre = idGenre
        self.genreType = genreType
        self.genreValue = genreValue

    def drop(self):
        db.session.delete(self)
        db.session.commit()

# BETA!
class recommendationAlgorithmTVContent(db.Model):
    __tablename__ = 'recommendationalgorithmtvcontent'
    idAlgorithm = ID_COLUMN(default=str(id_generator(title='recomendation_algorithm_tv_content_', size=16)))
    idAccount = ID_COLUMN(foreign_key='account.idAccount')
    idProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idGenre = ID_COLUMN(foreign_key='tvgenrelist.idGenre')
    genreType = STRING_COLUMN() # 'MOVIE' or 'TV'
    genreValue = INTEGER_COLUMN()
    def __init__(self, idAccount, idProfile, idGenre, genreType, genreValue):
        self.idAlgorithm = str(id_generator(title='recomendation_algorithm_tv_content_', size=16))
        self.idAccount = idAccount
        self.idProfile = idProfile
        self.idGenre = idGenre
        self.genreType = genreType
        self.genreValue = genreValue

    def drop(self):
        db.session.delete(self)
        db.session.commit()
"""
