# -*- encoding: utf-8 -*-
from import_parent import *
from termcolor import colored

# ! WORKING ON IT !
### TODO: by each content check players
# if there is a local player then pass
# else use scrape script to fetch local player

class LocalizePlayers():
    def __init__(self):
        self.PROFILE = {
                'idProfile': 'profile_21VZhSJFIwdNT6g4iGkS743opuMQG3ft1W',
                'idAccount': 'account_21JKmYvyAHvq1o6oK4JYpKNaBhDZO7pNgj',
        }
        self.movie = self.Movie(profile=self.PROFILE)
        self.tv = self.TV()
        self.movie.check()
        #self.tv.check()

    class Movie:
        def __init__(self, profile):
            self.PROFILE = {
                    'idProfile': profile['idProfile'],
                    'idAccount': profile['idAccount'],
            }

        def check(self):
            print(colored('[movie]', attrs=['bold', 'blink']))
            time.sleep(2)
            for _content in content.query.filter_by(type='MOVIE').all():
                if not len(moviePlayer.query.filter_by(idContent=_content.idContent).all()) >= 1:
                    db.session.add(moviePlayer(
                        idContent = _content.idContent,
                        idAddProfile = self.PROFILE['idProfile'],
                        idAddAccount = self.PROFILE['idAccount'],
                        language = 'ORIGINAL',
                        source = 'https://google.com',
                        title = 'TEST',
                        type = 'IFRAME',
                        visibility = 1,
                        order = 1,
                        lastEditDate = datetime.now(),
                    ))
                    print('added original player')
                    db.session.commit()
                if not moviePlayer.query.filter(and_(moviePlayer.idContent == _content.idContent, moviePlayer.language == 'DUBBED')).first():
                    print(colored("couldn't find local player", 'red', attrs=['bold']))
                else:
                    print(colored("found local player", 'green', attrs=['bold']))

    class TV:
        def check(self):
            print(colored('[tv]', attrs=['bold', 'blink']))
            time.sleep(2)
            for _content in content.query.filter_by(type='TV').all():
                if not tvPlayer.query.filter(and_(tvPlayer.idContent == _content.idContent, tvPlayer.language == 'DUBBED')).first():
                    print(colored("couldn't find local player", 'red', attrs=['bold']))
                else:
                    print(colored("found local player", 'green', attrs=['bold']))

LocalizePlayers()
