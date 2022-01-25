# -*- encoding: utf-8 -*-
from includes import *

"""
'content' table was created to list movies and tv's
in the homepage at the sametime. so that's why we
get all the values by hand.
"""

class content(db.Model):
    __tablename__ = 'content'
    idContent = ID_COLUMN(default=str(id_generator(title='content_', size=32)))
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    type = STRING_COLUMN() # 'MOVIE' or 'TV'
    title = STRING_COLUMN()
    titleOriginal = STRING_COLUMN()
    titleUrl = STRING_COLUMN()
    overview = STRING_COLUMN(size=2048, nullable=True)
    idTmdb = STRING_COLUMN(nullable=True)
    idImdb = STRING_COLUMN(nullable=True)
    imagePoster = STRING_COLUMN(size=2048, nullable=True)
    imageBackground = STRING_COLUMN(size=2048, nullable=True)
    adult = INTEGER_COLUMN(default=0)
    visibility = INTEGER_COLUMN(default=1)
    voteAverage = INTEGER_COLUMN()
    visitCount = INTEGER_COLUMN(nullable=True)
    releaseDate = STRING_COLUMN(nullable=True)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idAddProfile, idAddAccount, type, title, titleOriginal, titleUrl, overview, idTmdb, idImdb, imagePoster, imageBackground, adult, visibility, voteAverage, releaseDate, lastEditDate):
        self.idContent = str(id_generator(title='content_', size=32))
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.type = type
        self.title = title
        self.titleOriginal = titleOriginal
        self.titleUrl = titleUrl
        self.overview = overview
        self.idTmdb = idTmdb
        self.idImdb = idImdb
        self.imagePoster = imagePoster
        self.imageBackground = imageBackground
        self.adult = adult
        self.visibility = visibility
        self.voteAverage = voteAverage
        self.visitCount = 0
        self.releaseDate = releaseDate
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

        #### FOLDER
        content_dir = os.path.join(STORAGE_PATH, 'content', self.idContent)
        # mkdir: /storage/content/{{idContent}}
        if not os.path.exists(content_dir): os.makedirs(content_dir)
        #### END FOLDER

    # beta
    def get_tmdb_image_poster_to_local(self):
        import uuid
        if self.imagePoster.startswith('http'):
            new_img_name = str(uuid.uuid4()) + '.jpg'
            new_img_url = '/storage/content/{content_id}/{img_name}'.format(content_id=self.idContent, img_name=new_img_name)
            img_save_path = os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', self.idContent, new_img_name)
            os.system('curl {tmdb_img_url} > {local_img_path}'.format(tmdb_img_url=self.imagePoster, local_img_path=img_save_path))
            self.imagePoster = new_img_url
            db.session.commit()

    # beta
    def get_tmdb_image_background_to_local(self):
        import uuid
        if self.imageBackground.startswith('http'):
            new_img_name = str(uuid.uuid4()) + '.jpg'
            new_img_url = '/storage/content/{content_id}/{img_name}'.format(content_id=self.idContent, img_name=new_img_name)
            img_save_path = os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', self.idContent, new_img_name)
            os.system('curl {tmdb_img_url} > {local_img_path}'.format(tmdb_img_url=self.imageBackground, local_img_path=img_save_path))
            self.imageBackground = new_img_url
            db.session.commit()

    def get_genres(self):
        if self.type == 'MOVIE': return movieContentGenre.query.filter_by(idContent=self.idContent).all()
        elif self.type == 'TV': return tvContentGenre.query.filter_by(idContent=self.idContent).all()

    def drop(self):
        #### FOLDER
        content_dir = os.path.join(STORAGE_PATH, 'content', self.idContent)
        os.system('rm -rf ' + content_dir)
        #### END FOLDER

        for get_tag in contentTag.query.filter_by(idContent=self.idContent).all():
            get_tag.drop()

        for get_highlight in highlightContent.query.filter_by(idContent=self.idContent).all():
            get_highlight.drop()

        for get_collection_item in collectionItem.query.filter_by(idContent=self.idContent).all():
            get_collection_item.drop()

        if self.type == 'MOVIE':
            for get_comment in movieComment.query.filter_by(idContent=self.idContent).all():
                get_comment.drop()

            for get_player in moviePlayer.query.filter_by(idContent=self.idContent).all():
                get_player.drop()

            for get_content_genre in movieContentGenre.query.filter_by(idContent=self.idContent).all():
                get_content_genre.drop()

        if self.type == 'TV':
            for get_season_content in tvSeasonContent.query.filter_by(idContent=self.idContent).all():
                get_season_content.drop()

            for get_content_genre in tvContentGenre.query.filter_by(idContent=self.idContent).all():
                get_content_genre.drop()

        for get_language in contentLanguage.query.filter_by(idContent=self.idContent).all():
            get_language.drop()

        for get_country in contentCountry.query.filter_by(idContent=self.idContent).all():
            get_country.drop()

        for get_content_cast in contentCast.query.filter_by(idContent=self.idContent).all():
            get_content_cast.drop()

        db.session.delete(self)
        db.session.commit()

class contentTag(db.Model):
    __tablename__ = 'contenttag'
    idContentTag = ID_COLUMN(default=str(id_generator(title='content_tag_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    title = STRING_COLUMN()
    createDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, title):
        self.idContentTag = str(id_generator(title='content_tag_', size=32))
        self.idContent = idContent
        self.title = title
        self.createDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class highlightContent(db.Model):
    __tablename__ = 'highlightcontent'
    idHighlight = ID_COLUMN(default=str(id_generator(title='highlight_content_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    highlightDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idAddProfile, idAddAccount):
        self.idHighlight = str(id_generator(title='highlight_content_', size=32))
        self.idContent = idContent
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.highlightDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class latestWatchedEpisode(db.Model):
    __tablename__ = 'latestwatchedepisode'
    idLWEpisode = ID_COLUMN(default=str(id_generator(title='l_w_episode_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idTvSeason = ID_COLUMN(foreign_key='tvseasoncontent.idTvSeason')
    idTvEpisode = ID_COLUMN(foreign_key='tvepisodecontent.idTvEpisode')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    watchDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idTvSeason, idTvEpisode, idAddProfile, idAddAccount):
        self.idLWEpisode = str(id_generator(title='l_w_episode_', size=32))
        self.idContent = idContent
        self.idTvSeason = idTvSeason
        self.idTvEpisode = idTvEpisode
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.watchDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class tvSeasonContent(db.Model):
    __tablename__ = 'tvseasoncontent'
    idTvSeason = ID_COLUMN(default=str(id_generator(title='tv_season_content_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    title = STRING_COLUMN(nullable=True)
    overview = STRING_COLUMN(size=2048, nullable=True)
    idTmdb = STRING_COLUMN(nullable=True)
    imagePoster = STRING_COLUMN(size=2048, nullable=True)
    seasonNumber = INTEGER_COLUMN()
    visibility = INTEGER_COLUMN(default=1)
    visitCount = INTEGER_COLUMN(nullable=True)
    airDate = STRING_COLUMN(nullable=True)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idAddProfile, idAddAccount, title, overview, idTmdb, imagePoster, seasonNumber, visibility, airDate, lastEditDate):
        self.idTvSeason = str(id_generator(title='tv_season_content_', size=32))
        self.idContent = idContent
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.title = title
        self.overview = overview
        self.idTmdb = idTmdb
        self.imagePoster = imagePoster
        self.seasonNumber = seasonNumber
        self.visibility = visibility
        self.visitCount = 0
        self.airDate = airDate
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def get_content(self): return content.query.filter_by(idContent=self.idContent).first()

    # beta
    def get_tmdb_image_poster_to_local(self):
        import uuid
        if self.imagePoster.startswith('http'):
            new_img_name = str(uuid.uuid4()) + '.jpg'
            new_img_url = '/storage/content/{content_id}/{img_name}'.format(content_id=self.idContent, img_name=new_img_name)
            img_save_path = os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', self.idContent, new_img_name)
            os.system('curl {tmdb_img_url} > {local_img_path}'.format(tmdb_img_url=self.imagePoster, local_img_path=img_save_path))
            self.imagePoster = new_img_url
            db.session.commit()

    # beta
    def change_season_number(self, new_season_number):
        return 1

    def drop(self):
      for get_episode in tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == self.idContent, tvEpisodeContent.idTvSeason == self.idTvSeason)).all():
          get_episode.drop()

      for get_title_comment in tvTitleComment.query.filter(and_(tvTitleComment.idContent == self.idContent, tvTitleComment.idTvSeason == self.idTvSeason)).all():
          get_title_comment.drop()

      db.session.delete(self)
      db.session.commit()

class tvEpisodeContent(db.Model):
    __tablename__ = 'tvepisodecontent'
    idTvEpisode = ID_COLUMN(default=str(id_generator(title='tv_episode_content_', size=32)))
    idTvSeason = ID_COLUMN(foreign_key='tvseasoncontent.idTvSeason')
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    title = STRING_COLUMN(nullable=True)
    overview = STRING_COLUMN(size=2048, nullable=True)
    idTmdb = STRING_COLUMN(nullable=True)
    idImdb = STRING_COLUMN(nullable=True)
    imagePoster = STRING_COLUMN(size=2048, nullable=True)
    seasonNumber = INTEGER_COLUMN()
    episodeNumber = INTEGER_COLUMN()
    visibility = INTEGER_COLUMN(default=1)
    voteAverage = INTEGER_COLUMN()
    visitCount = INTEGER_COLUMN(nullable=True)
    airDate = STRING_COLUMN(nullable=True)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idTvSeason, idContent, idAddProfile, idAddAccount, title, overview, idTmdb, idImdb, imagePoster, seasonNumber, episodeNumber, visibility, voteAverage, airDate, lastEditDate):
        self.idTvEpisode = str(id_generator(title='tv_episode_content_', size=32))
        self.idTvSeason = idTvSeason
        self.idContent = idContent
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.title = title
        self.overview = overview
        self.idTmdb = idTmdb
        self.idImdb = idImdb
        self.imagePoster = imagePoster
        self.seasonNumber = seasonNumber
        self.episodeNumber = episodeNumber
        self.visibility = visibility
        self.voteAverage = voteAverage
        self.visitCount = 0
        self.airDate = airDate
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def get_content(self): return content.query.filter_by(idContent=self.idContent).first()
    def get_season(self): return tvSeasonContent.query.filter_by(idTvSeason=self.idTvSeason).first()

    # beta
    def get_tmdb_image_poster_to_local(self):
        import uuid
        if self.imagePoster.startswith('http'):
            new_img_name = str(uuid.uuid4()) + '.jpg'
            new_img_url = '/storage/content/{content_id}/{img_name}'.format(content_id=self.idContent, img_name=new_img_name)
            img_save_path = os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', self.idContent, new_img_name)
            os.system('curl {tmdb_img_url} > {local_img_path}'.format(tmdb_img_url=self.imagePoster, local_img_path=img_save_path))
            self.imagePoster = new_img_url
            db.session.commit()

    def get_next_episode(self):
        next_episode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idTvSeason == self.idTvSeason, tvEpisodeContent.idContent == self.idContent, tvEpisodeContent.seasonNumber == self.seasonNumber, tvEpisodeContent.episodeNumber == self.episodeNumber + 1)).first()
        if not next_episode:
            return False

        return next_episode

    def get_previous_episode(self):
        previous_episode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idTvSeason == self.idTvSeason, tvEpisodeContent.idContent == self.idContent, tvEpisodeContent.seasonNumber == self.seasonNumber, tvEpisodeContent.episodeNumber == self.episodeNumber - 1)).first()
        if not previous_episode:
            return False

        return previous_episode

    """
    [ # beta ]
    what do we need to do?
    ===================
    for each 'tvepisodecontent', 'tvplayer', 'latestwatchedepisode', 'tvcomment', 'tvcommentrate' that belongs to this episode
    we need to update `episodeNumber` and `idTvEpisode` (!)
    cells
    BUT FIRST, you need to check if an episode with 'new_episode_number' exists
    """
    def change_episode_number(self, new_episode_number):
        if tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == self.idContent,
                                            tvEpisodeContent.idTvSeason == self.idTvSeason,
                                            tvEpisodeContent.seasonNumber == self.seasonNumber,
                                            tvEpisodeContent.episodeNumber == new_episode_number)).first():
            return False

        self.episodeNumber = new_episode_number

        for get_player in tvPlayer.query.filter(and_(tvPlayer.idContent == self.idContent,
                                                    tvPlayer.idTvSeason == self.idTvSeason,
                                                    tvPlayer.idTvEpisode == self.idTvEpisode,
                                                    tvPlayer.seasonNumber == self.seasonNumber)).all():
            print(get_player.title)
            get_player.episodeNumber = new_episode_number

        print('')
        for get_l_w_episode in latestWatchedEpisode.query.filter(and_(latestWatchedEpisode.idContent == self.idContent,
                                                                    latestWatchedEpisode.idTvSeason == self.idTvSeason,
                                                                    latestWatchedEpisode.idTvEpisode == self.idTvEpisode)).all():
            print(get_l_w_episode.idLWEpisode)

        print('')
        for get_comment in tvComment.query.filter(and_(tvComment.idContent == self.idContent,
                                                    tvComment.idTvSeason == self.idTvSeason,
                                                    tvComment.idTvEpisode == self.idTvEpisode)).all():
            print(get_comment.text)

        print('')
        for get_comment_rate in tvCommentRate.query.filter(and_(tvCommentRate.idContent == self.idContent,
                                                                tvCommentRate.idTvSeason == self.idTvSeason,
                                                                tvCommentRate.idTvEpisode == self.idTvEpisode)).all():
            print(get_comment_rate.rateType)

        db.session.commit()

        return

    def drop(self):
        for get_comment in tvComment.query.filter(and_(tvComment.idContent == self.idContent, tvComment.idTvSeason == self.idTvSeason, tvComment.idTvEpisode == self.idTvEpisode)).all():
            get_comment.drop()

        for get_player in tvPlayer.query.filter(and_(tvPlayer.idContent == self.idContent, tvPlayer.seasonNumber == self.seasonNumber, tvPlayer.episodeNumber == self.episodeNumber)).all():
            get_player.drop()

        for get_latest_watched_episode in latestWatchedEpisode.query.filter_by(idTvEpisode=self.idTvEpisode).all():
            get_latest_watched_episode.drop()

        db.session.delete(self)
        db.session.commit()

class movieComment(db.Model):
    __tablename__ = 'moviecomment'
    idComment = ID_COLUMN(default=str(id_generator(title='movie_comment_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    text = STRING_COLUMN(size=512)
    replyTo = STRING_COLUMN(nullable=True)
    visibility = INTEGER_COLUMN(default=1)
    spoiler = INTEGER_COLUMN(default=0)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idAddProfile, idAddAccount, text, replyTo, visibility, spoiler, lastEditDate):
        self.idComment = str(id_generator(title='movie_comment_', size=32))
        self.idContent = idContent
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.text = text
        self.replyTo = replyTo
        self.visibility = visibility
        self.spoiler = spoiler
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        for get_comment_rate in movieCommentRate.query.filter_by(idComment=self.idComment).all():
            get_comment_rate.drop()

        for get_comment_replyto in movieComment.query.filter_by(replyTo=self.idComment).all():
            get_comment_replyto.drop()

        db.session.delete(self)
        db.session.commit()

class tvComment(db.Model):
    __tablename__ = 'tvcomment'
    idComment = ID_COLUMN(default=str(id_generator(title='tv_comment_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idTvSeason = ID_COLUMN(foreign_key='tvseasoncontent.idTvSeason')
    idTvEpisode = ID_COLUMN(foreign_key='tvepisodecontent.idTvEpisode')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    text = STRING_COLUMN(size=512)
    replyTo = STRING_COLUMN(nullable=True)
    visibility = INTEGER_COLUMN(default=1)
    spoiler = INTEGER_COLUMN(default=0)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idTvSeason, idTvEpisode, idAddProfile, idAddAccount, text, replyTo, visibility, spoiler, lastEditDate):
        self.idComment = str(id_generator(title='tv_comment_', size=32))
        self.idContent = idContent
        self.idTvSeason = idTvSeason
        self.idTvEpisode = idTvEpisode
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.text = text
        self.replyTo = replyTo
        self.visibility = visibility
        self.spoiler = spoiler
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        for get_comment_rate in tvCommentRate.query.filter_by(idComment=self.idComment).all():
            get_comment_rate.drop()

        for get_comment_replyto in tvComment.query.filter_by(replyTo=self.idComment).all():
            get_comment_replyto.drop()

        db.session.delete(self)
        db.session.commit()

class tvTitleComment(db.Model):
    __tablename__ = 'tvtitlecomment'
    idComment = ID_COLUMN(default=str(id_generator(title='tv_title_comment_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idTvSeason = ID_COLUMN(foreign_key='tvseasoncontent.idTvSeason')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    text = STRING_COLUMN(size=512)
    replyTo = STRING_COLUMN(nullable=True)
    visibility = INTEGER_COLUMN(default=1)
    spoiler = INTEGER_COLUMN(default=0)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idTvSeason, idAddProfile, idAddAccount, text, replyTo, visibility, spoiler, lastEditDate):
        self.idComment = str(id_generator(title='tv_title_comment_', size=32))
        self.idContent = idContent
        self.idTvSeason = idTvSeason
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.text = text
        self.replyTo = replyTo
        self.visibility = visibility
        self.spoiler = spoiler
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        for get_title_comment_rate in tvTitleCommentRate.query.filter_by(idComment=self.idComment).all():
            get_title_comment_rate.drop()

        for get_title_comment_replyto in tvTitleComment.query.filter_by(replyTo=self.idComment).all():
            get_title_comment_replyto.drop()

        db.session.delete(self)
        db.session.commit()

class movieCommentRate(db.Model):
    __tablename__ = 'moviecommentrate'
    idRate = ID_COLUMN(default=str(id_generator(title='movie_comment_rate_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idComment = ID_COLUMN(foreign_key='moviecomment.idComment')
    idRateProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idRateAccount = ID_COLUMN(foreign_key='account.idAccount')
    rateType = STRING_COLUMN(default='LIKE')
    rateDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idComment, idRateProfile, idRateAccount, rateType):
        self.idRate = str(id_generator(title='movie_comment_rate_', size=32))
        self.idContent = idContent
        self.idComment = idComment
        self.idRateProfile = idRateProfile
        self.idRateAccount = idRateAccount
        self.rateType = rateType
        self.rateDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class tvCommentRate(db.Model):
    __tablename__ = 'tvcommentrate'
    idRate = ID_COLUMN(default=str(id_generator(title='tv_comment_rate_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idTvSeason = ID_COLUMN(foreign_key='tvseasoncontent.idTvSeason')
    idTvEpisode = ID_COLUMN(foreign_key='tvepisodecontent.idTvEpisode')
    idComment = ID_COLUMN(foreign_key='tvcomment.idComment')
    idRateProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idRateAccount = ID_COLUMN(foreign_key='account.idAccount')
    rateType = STRING_COLUMN(default='LIKE')
    rateDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idTvSeason, idTvEpisode, idComment, idRateProfile, idRateAccount, rateType):
      self.idRate = str(id_generator(title='tv_comment_rate_', size=32))
      self.idContent = idContent
      self.idTvSeason = idTvSeason
      self.idTvEpisode = idTvEpisode
      self.idComment = idComment
      self.idRateProfile = idRateProfile
      self.idRateAccount = idRateAccount
      self.rateType = rateType
      self.rateDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class tvTitleCommentRate(db.Model):
    __tablename__ = 'tvtitlecommentrate'
    idRate = ID_COLUMN(default=str(id_generator(title='tv_title_comment_rate_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idTvSeason = ID_COLUMN(foreign_key='tvseasoncontent.idTvSeason')
    idComment = ID_COLUMN(foreign_key='tvtitlecomment.idComment')
    idRateProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idRateAccount = ID_COLUMN(foreign_key='account.idAccount')
    rateType = STRING_COLUMN(default='LIKE')
    rateDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idTvSeason, idComment, idRateProfile, idRateAccount, rateType):
      self.idRate = str(id_generator(title='tv_title_comment_rate_', size=32))
      self.idContent = idContent
      self.idTvSeason = idTvSeason
      self.idComment = idComment
      self.idRateProfile = idRateProfile
      self.idRateAccount = idRateAccount
      self.rateType = rateType
      self.rateDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()
