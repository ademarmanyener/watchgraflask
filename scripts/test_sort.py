# -*- encoding: utf-8 -*-
from import_parent import *

# IT WORKS!

def test():
    #for _ in content.query.filter(and_(content.type == 'MOVIE', contentCountry.idISO_3166_1 == 'TR')).all():
    for _ in db.session.query(content).join(contentCountry).join(contentLanguage).filter(content.type == 'TV', contentCountry.idISO_3166_1 == 'TR', contentLanguage.idISO_639_1 == 'en').all():
        print(' ==> {} --- {}'.format(_.title))

test()
