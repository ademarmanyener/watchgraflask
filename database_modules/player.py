# -*- encoding: utf-8 -*-
from includes import *

"""

this section is for players

language: 'DUBBED', 'SUBBED', 'ORIGINAL'
type: 'IFRAME', 'VIDEOJS', 'PLYR', 'TRAILER'

"""

class moviePlayer(db.Model):
    __tablename__ = 'movieplayer'
    idPlayer = ID_COLUMN(default=str(id_generator(title='movie_player_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    language = STRING_COLUMN(nullable=True)
    source = STRING_COLUMN(size=5120)
    title = STRING_COLUMN()
    viewKey = STRING_COLUMN()
    type = STRING_COLUMN()
    visibility = INTEGER_COLUMN(default=1)
    order = INTEGER_COLUMN(default=1)
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idContent, idAddProfile, idAddAccount, language, source, title, type, visibility, order, lastEditDate):
        self.idPlayer = str(id_generator(title='movie_player_', size=32))
        self.idContent = idContent
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.language = language
        self.source = source
        self.title = title
        self.viewKey = str(id_generator(size=6))
        self.type = type
        self.visibility = visibility
        self.order = order
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class tvPlayer(db.Model):
    __tablename__ = 'tvplayer'
    idPlayer = ID_COLUMN(default=str(id_generator(title='tv_player_', size=32)))
    idTvSeason = ID_COLUMN(foreign_key='tvseasoncontent.idTvSeason')
    idTvEpisode = ID_COLUMN(foreign_key='tvepisodecontent.idTvEpisode')
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    language = STRING_COLUMN(nullable=True)
    source = STRING_COLUMN(size=5120)
    title = STRING_COLUMN()
    viewKey = STRING_COLUMN()
    type = STRING_COLUMN()
    visibility = INTEGER_COLUMN(default=1)
    order = INTEGER_COLUMN(default=1)
    seasonNumber = INTEGER_COLUMN()
    episodeNumber = INTEGER_COLUMN()
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idTvSeason, idTvEpisode, idContent, idAddProfile, idAddAccount, language, source, title, type, visibility, order, seasonNumber, episodeNumber, lastEditDate):
        self.idPlayer = str(id_generator(title='tv_player_', size=32))
        self.idTvSeason = idTvSeason
        self.idTvEpisode = idTvEpisode
        self.idContent = idContent
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount
        self.language = language
        self.source = source
        self.title = title
        self.viewKey = str(id_generator(size=6))
        self.type = type
        self.visibility = visibility
        self.order = order
        self.seasonNumber = seasonNumber
        self.episodeNumber = episodeNumber
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()
