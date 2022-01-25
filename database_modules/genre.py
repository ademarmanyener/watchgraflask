# -*- encoding: utf-8 -*-
from includes import *

class movieGenreList(db.Model):
    __tablename__ = 'moviegenrelist'
    idGenre = ID_COLUMN()
    title = STRING_COLUMN()
    titleOriginal = STRING_COLUMN()
    def __init__(self, idGenre, title, titleOriginal):
        self.idGenre = idGenre
        self.title = title
        self.titleOriginal = titleOriginal

    def drop(self):
        for get_content_genre in movieContentGenre.query.filter_by(idGenre=self.idGenre).all():
            get_content_genre.drop()

        db.session.delete(self)
        db.session.commit()

class tvGenreList(db.Model):
    __tablename__ = 'tvgenrelist'
    idGenre = ID_COLUMN()
    title = STRING_COLUMN()
    titleOriginal = STRING_COLUMN()
    def __init__(self, idGenre, title, titleOriginal):
        self.idGenre = idGenre
        self.title = title
        self.titleOriginal = titleOriginal

    def drop(self):
        for get_content_genre in tvContentGenre.query.filter_by(idGenre=self.idGenre).all():
            get_content_genre.drop()

        db.session.delete(self)
        db.session.commit()

class movieContentGenre(db.Model):
    __tablename__ = 'moviecontentgenre'
    idContentGenre = ID_COLUMN(default=str(id_generator(title='movie_content_genre_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idGenre = ID_COLUMN(foreign_key='moviegenrelist.idGenre')
    def __init__(self, idContent, idGenre):
        self.idContentGenre = str(id_generator(title='movie_content_genre_', size=32))
        self.idContent = idContent
        self.idGenre = idGenre

    def get_title(self): return movieGenreList.query.filter_by(idGenre=self.idGenre).first().title
    def get_titleOriginal(self): return movieGenreList.query.filter_by(idGenre=self.idGenre).first().titleOriginal

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class tvContentGenre(db.Model):
    __tablename__ = 'tvcontentgenre'
    idContentGenre = ID_COLUMN(default=str(id_generator(title='tv_content_genre_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idGenre = ID_COLUMN(foreign_key='tvgenrelist.idGenre')
    def __init__(self, idContent, idGenre):
        self.idContentGenre = str(id_generator(title='tv_content_genre_', size=32))
        self.idContent = idContent
        self.idGenre = idGenre

    def get_title(self): return tvGenreList.query.filter_by(idGenre=self.idGenre).first().title
    def get_titleOriginal(self): return tvGenreList.query.filter_by(idGenre=self.idGenre).first().titleOriginal

    def drop(self):
        db.session.delete(self)
        db.session.commit()
