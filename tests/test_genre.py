# -*- encoding: utf-8 -*-
from includes import *

TMDB_ID = '120'


for c in content.content.query.filter_by(type='MOVIE').all(): 
    print(c.idContent + ' -- ' + str(len(moviePlayer.query.filter_by(idContent=c.idContent).all())))
