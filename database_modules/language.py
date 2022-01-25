# -*- encoding: utf-8 -*-
from includes import *

# instead of idLanguage
# use idISO_639_1 
class languageList(db.Model):
    __tablename__ = 'languagelist'
    idISO_639_1 = ID_COLUMN()
    title = STRING_COLUMN()
    titleOriginal = STRING_COLUMN()
    def __init__(self, idISO_639_1, title, titleOriginal):
        self.idISO_639_1 = idISO_639_1 
        self.title = title
        self.titleOriginal = titleOriginal

    def drop(self):
        for get_content_language in contentLanguage.query.filter_by(idISO_639_1=self.idISO_639_1).all():
            get_content_language.drop()

        db.session.delete(self)
        db.session.commit()

class contentLanguage(db.Model):
    __tablename__ = 'contentlanguage'
    idContentLanguage = ID_COLUMN(default=str(id_generator(title='content_language_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idISO_639_1 = ID_COLUMN(foreign_key='languagelist.idISO_639_1')
    def __init__(self, idContent, idISO_639_1):
        self.idContentLanguage = str(id_generator(title='content_language_', size=32))
        self.idContent = idContent
        self.idISO_639_1 = idISO_639_1

    def drop(self):
        db.session.delete(self)
        db.session.commit()