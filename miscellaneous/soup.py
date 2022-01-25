# -*- encoding: utf-8 -*-
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys, time, os

VERSION = 'v0.0.4.5'

# 'https://www.filmyani.com/'
class Soup_Local:
    query = ''
    fetch_method = 'html5lib'
    def __init__(self, query):
        self.query = query

    def Movie(self):
        if self.get_first_item_href(get_query=self.query) != 1:
            if self.get_movie_player_src(get_url=self.get_first_item_href(get_query=self.query)) != 1:
                return self.get_movie_player_src(get_url=self.get_first_item_href(get_query=self.query))
            else: return 1
        else: return 1

    def get_movie_player_src(self, get_url):
        req = requests.get(get_url)
        soup = BeautifulSoup(req.text, self.fetch_method)

        try:
            try: title = soup.title.string
            except: title = 'No Item Title'

            try:
                return soup.find('div', id='video').find('div', id='videos').find('span', id='plyg').find('iframe').get('src')
            except: return 1
        except: return 1

    def get_first_item_href(self, get_query):
        req = requests.get('https://www.filmyani.com/?s=' + get_query)
        soup = BeautifulSoup(req.text, self.fetch_method)

        try:
            try: title = soup.title.string
            except: title = 'No Item List Title'

            try:
                items = soup.find('div', class_='sayfa-sol').find('div', class_='icerik').find_all('div', class_='frag-k')
                if len(items) > 0: return items[0].find('a', class_='resim').get('href')
                else: return 1
            except: return 1
        except: return 1

# 'https://www.hdfilmcehennemi2.pw/'
# W.I.P.
class Soup_Local_2:
    query = ''
    fetch_method = 'html5lib'
    def __init__(self, query):
        self.query = query

    def Movie(self):
        if self.get_first_item_href(get_query=self.query) != 1:
            if self.get_movie_player_src(get_url=self.get_first_item_href(get_query=self.query)) != 1:
                return self.get_movie_player_src(get_url=self.get_first_item_href(get_query=self.query))
            else: return 1
        else: return 1

    def get_movie_player_src(self, get_url):
        req = requests.get(get_url)
        soup = BeautifulSoup(req.text, self.fetch_method)

        try:
            try: title = soup.title.string
            except: title = 'No Item Title'

            print('             ==> ' + title)
            print('\n\n\n\n\n\n\n\n')
            f = open('test.txt', 'w')
            f.writeline(soup)
            f.close()
            print('\n\n\n\n\n\n\n\n')


            try:
                #return soup.find('div', id='video').find('div', id='videos').find('span', id='plyg').find('iframe').get('src')
                return soup.find('div', class_='filmicerik').find('iframe').get('src')
            except: return 3
        except: return 3

    def get_first_item_href(self, get_query):
        req = requests.get('https://www.hdfilmcehennemi2.pw/?arama=' + get_query)
        soup = BeautifulSoup(req.text, self.fetch_method)

        try:
            try: title = soup.title.string
            except: title = 'No Item List Title'

            try:
                items = soup.find('div', class_='filmborder').find('div', class_='filmcontent').find_all('div', class_='moviefilm')
                if len(items) > 0: return items[0].find('a').get('href')
                else: return 1
            except: return 1
        except: return 1

# 'https://www3.soap2dayto.org/'
class Soup_Global:
    query = ''
    fetch_method = 'html5lib'
    def __init__(self, query):
        self.query = query.replace(' ', '-')

    def Movie(self):
        if self.get_first_item_href(get_query=self.query) != 1:
            if self.get_movie_player_src(get_url=self.get_first_item_href(get_query=self.query)) != 1:
                return self.get_movie_player_src(get_url=self.get_first_item_href(get_query=self.query))
            else: return 1
        else: return 1

    def TV(self, tmdb_id, season_number, episode_number):
        return self.get_tv_player_src(tmdb_id, season_number, episode_number)

        if self.get_first_item_href(get_query=self.query) != 1:
            if self.get_tv_player_src(get_url=self.get_first_item_href(get_query=self.query)) != 1:
                return self.get_tv_player_src(get_url=self.get_first_item_href(get_query=self.query))
            else: return 1
        else: return 1

    def get_movie_player_src(self, get_url):
        req = requests.get('https://www3.soap2dayto.org' + get_url)
        soup = BeautifulSoup(req.text, self.fetch_method)

        try:
            try: title = soup.title.string
            except: title = 'No Item Title'

            try:
                return soup.find('div', id='main-wrapper').find('div', class_='detail_page detail_page-style').find('div', class_='container').find('div', class_='detail_page-watch').find('div', class_='watching_player').find('div', id='watch-iframe').find('iframe', id='iframe-embed').get('src')
                return 0
            except: return 1
        except: return 1

    # BETA
    def get_tv_player_src(self, tmdb_id, season_number, episode_number):
        return 'https://www.2embed.ru/embed/tmdb/tv?id='+tmdb_id+'&s='+season_number+'&e='+episode_number

        req = requests.get('https://www3.soap2dayto.org' + get_url)
        soup = BeautifulSoup(req.text, self.fetch_method)

        try:
            try: title = soup.title.string
            except: title = 'No Item Title'

            try:
                return soup.find('div', id='main-wrapper').find('div', class_='detail_page detail_page-style').find('div', class_='container').find('div', class_='detail_page-watch').find('div', class_='watching_player').find('div', id='watch-iframe').find('iframe', id='iframe-embed').get('src')
                return 0
            except: return 2
        except: return 2

    def get_first_item_href(self, get_query):
        req = requests.get('https://www3.soap2dayto.org/search/' + get_query)
        soup = BeautifulSoup(req.text, self.fetch_method)

        try:
            try: title = soup.title.string
            except: title = 'No Item List Title'

            try:
                items = soup.find('div', class_='block_area-content block_area-list film_list film_list-grid').find('div', class_='film_list-wrap').find_all('div', class_='flw-item')
                if len(items) > 0: return items[0].find('div', class_='film-poster').find('a', class_='film-poster-ahref flw-item-tip').get('href')
                else: return 1
            except: return 1
        except: return 1

class soup_global_beta:
    def get_movie_player_src(tmdb_id): return 'https://www.2embed.ru/embed/tmdb/movie?id=' + str(tmdb_id)
    def get_tv_player_src(tmdb_id, season_number, episode_number): return 'https://www.2embed.ru/embed/tmdb/tv?id=' + str(tmdb_id) + '&s=' + str(season_number) + '&e=' + str(episode_number)

if __name__ == '__main__':
    if sys.argv[1] == '--movie': print(soup_global_beta.get_movie_player_src(tmdb_id=sys.argv[2]))
    if sys.argv[1] == '--tv': print(soup_global_beta.get_tv_player_src(tmdb_id=sys.argv[2], season_number=sys.argv[3], episode_number=sys.argv[4]))