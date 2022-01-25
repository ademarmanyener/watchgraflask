# -*- encoding: utf-8 -*-
from includes import *

# instead of idCountry 
# use idISO_3166_1 
class countryList(db.Model):
    __tablename__ = 'countrylist'
    idISO_3166_1 = ID_COLUMN()
    title = STRING_COLUMN()
    titleOriginal = STRING_COLUMN()
    def __init__(self, idISO_3166_1, title, titleOriginal):
        self.idISO_3166_1 = idISO_3166_1 
        self.title = title
        self.titleOriginal = titleOriginal

    def drop(self):
        for get_content_country in contentCountry.query.filter_by(idISO_3166_1=self.idISO_3166_1).all():
            get_content_country.drop()

        db.session.delete(self)
        db.session.commit()

class contentCountry(db.Model):
    __tablename__ = 'contentcountry'
    idContentCountry = ID_COLUMN(default=str(id_generator(title='content_country_', size=32)))
    idContent = ID_COLUMN(foreign_key='content.idContent')
    idISO_3166_1 = ID_COLUMN(foreign_key='countrylist.idISO_3166_1')
    def __init__(self, idContent, idISO_3166_1):
        self.idContentCountry = str(id_generator(title='content_country_', size=32))
        self.idContent = idContent
        self.idISO_3166_1 = idISO_3166_1

    def drop(self):
        db.session.delete(self)
        db.session.commit()