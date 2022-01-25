# -*- encoding: utf-8 -*-
import string

TITLE = """Driver's Licence: Due"""

def turnTitleUrl(get_title):
    print(get_title.lower().replace(' ', '-').replace("'", '').replace(':', ''))

turnTitleUrl(TITLE)
