# -*- encoding: utf-8 -*-
from includes import *

#############################################################
# ========================================================= #
# ========================================================= #
# routes for debugging begin
# ========================================================= #
# ========================================================= #
#############################################################

@app.route('/tmdbsimple/movie/2/popular/<page_begin>/<page_end>')
def tmdbsimple_movie2_popular(page_begin, page_end):
  get_profile = profile.query.filter(profile.permission != 'DOCKER').first()
  session['ACCOUNT'] = {
    "idAccount": get_profile.idAccount
  }
  session['PROFILE'] = {
    "idProfile": get_profile.idProfile,
    "permission": 'ADMIN'
  }
  for get_page in range(int(page_begin), int(page_end)):
    for get_popular in tmdb.Movies().popular(language=TMDB_LANGUAGE, page=get_page)['results']:
      TMDBSimpleasy.Movie.addContent(get_tmdb_id=get_popular['id'])
      for get_cast in tmdb.Movies(get_popular['id']).credits(language=TMDB_LANGUAGE)['cast']:
        TMDBSimpleasy.Cast.addCast(get_cast['id'])
        if contentCast.query.filter(and_(contentCast.idContent == str(content.query.filter(and_(content.idTmdb == str(get_popular['id']), content.type == 'MOVIE')).first().idContent), contentCast.idCast == str(cast.query.filter_by(idTmdb=str(get_cast['id'])).first().idCast))).first() != None: pass
        else:
          db.session.add(contentCast(
            idContent = content.query.filter(and_(content.idTmdb == get_popular['id'], content.type == 'MOVIE')).first().idContent,
            idCast = cast.query.filter_by(idTmdb=str(get_cast['id'])).first().idCast,
            character = get_cast['character'],
            order = get_cast['order'],
          ))
      db.session.commit()
      TMDBSimpleasy.Movie.addPlayer(get_tmdb_id=get_popular['id'])
      time.sleep(3)
  return redirect(url_for('destroy_account'))

@app.route('/tmdbsimple/cast/add/<tmdb_id>')
def tmdbsimple_cast_add(tmdb_id):
    get_profile = profile.query.filter(profile.permission != 'DOCKER').first()
    session['ACCOUNT'] = {
      "idAccount": get_profile.idAccount 
    }
    session['PROFILE'] = {
      "idProfile": get_profile.idProfile,
      "permission": 'ADMIN'
    }
    TMDBSimpleasy.Cast.addCast(get_tmdb_id=tmdb_id)
    return redirect(url_for('destroy_account'))

@app.route('/tmdbsimple/movie/add/<tmdb_id>')
def tmdbsimple_movie_add(tmdb_id):
    get_profile = profile.query.filter(profile.permission != 'DOCKER').first()
    session['ACCOUNT'] = {
      "idAccount": get_profile.idAccount 
    }
    session['PROFILE'] = {
      "idProfile": get_profile.idProfile,
      "permission": 'ADMIN'
    }
    TMDBSimpleasy.Movie.addComprehensive(get_tmdb_id=tmdb_id)
    return redirect(url_for('destroy_account'))

@app.route('/tmdbsimple/tv/add/<tmdb_id>')
def tmdbsimple_tv_add(tmdb_id):
    get_profile = profile.query.filter(profile.permission != 'DOCKER').first()
    session['ACCOUNT'] = {
      "idAccount": get_profile.idAccount 
    }
    session['PROFILE'] = {
      "idProfile": get_profile.idProfile,
      "permission": 'ADMIN'
    }
    TMDBSimpleasy.TV.addComprehensive(get_tmdb_id=tmdb_id)
    return redirect(url_for('destroy_account'))

#############################################################
# ========================================================= #
# ========================================================= #
# routes for debugging end 
# ========================================================= #
# ========================================================= #
#############################################################

class TMDBSimpleasy:
  class Cast:
    def addCast(get_tmdb_id):
      #if not check_admin(): return 1

      SELECTED_ID_ADD_PROFILE = session['PROFILE']['idProfile']
      SELECTED_ID_ADD_ACCOUNT = session['ACCOUNT']['idAccount']
      SELECTED_GENDER = 0
      SELECTED_NAME = '#'
      SELECTED_NAME_URL = '#'
      SELECTED_BIOGRAPHY = '#'
      SELECTED_ID_TMDB = get_tmdb_id
      SELECTED_ID_IMDB = '#'
      SELECTED_ID_TWITTER = '#' 
      SELECTED_ID_INSTAGRAM = '#' 
      SELECTED_IMAGE_POSTER = '/static/img/defaults/poster_cast.png'
      SELECTED_ADULT = 0
      SELECTED_VISIBILITY = 1 
      SELECTED_BIRTH_PLACE = '#'
      SELECTED_BIRTH_DATE = '#'
      SELECTED_DEATH_DATE = '#'
      SELECTED_LAST_EDIT_DATE = datetime.now(pytz.timezone(PY_TIMEZONE))

      get_details = tmdb.People(get_tmdb_id).info(language=TMDB_LANGUAGE)
      get_external_ids = tmdb.People(get_tmdb_id).external_ids(language=TMDB_LANGUAGE)

      if get_details['gender'] != None: SELECTED_GENDER = get_details['gender']
      if get_details['name'] != None:
        SELECTED_NAME = get_details['name']
        #SELECTED_NAME_URL = get_details['name'].lower().replace(' ', '-').replace('.', '').replace(':', '').replace("'", '')
        SELECTED_NAME_URL = slugify(get_details['name'])
        if cast.query.filter(and_(cast.nameUrl == SELECTED_NAME_URL)).first() != None: SELECTED_NAME_URL = SELECTED_NAME_URL + '_' + id_generator(size=4)
      if get_details['biography'] != None: SELECTED_BIOGRAPHY = get_details['biography']
      if get_details['id'] != None: SELECTED_ID_TMDB = get_details['id']
      ### external ids
      if get_external_ids['imdb_id'] != None: SELECTED_ID_IMDB = get_external_ids['imdb_id']
      if get_external_ids['twitter_id'] != None: SELECTED_ID_TWITTER = get_external_ids['twitter_id']
      if get_external_ids['instagram_id'] != None: SELECTED_ID_INSTAGRAM = get_external_ids['instagram_id']
      ### end external ids
      if get_details['profile_path'] != None: SELECTED_IMAGE_POSTER = 'https://www.themoviedb.org/t/p/w300' + get_details['profile_path']
      if get_details['adult'] != None:
        #SELECTED_ADULT = get_details['adult']
        if get_details['adult']: SELECTED_ADULT = 1
      if get_details['place_of_birth'] != None: SELECTED_BIRTH_PLACE = get_details['place_of_birth']
      if get_details['birthday'] != None: SELECTED_BIRTH_DATE = get_details['birthday']
      if get_details['deathday'] != None: SELECTED_DEATH_DATE = get_details['deathday']

      if cast.query.filter(and_(cast.idTmdb == str(SELECTED_ID_TMDB))).first() != None: pass
      else:
        try:
            db.session.add(cast(
              idAddProfile = SELECTED_ID_ADD_PROFILE,
              idAddAccount = SELECTED_ID_ADD_ACCOUNT,
              gender = SELECTED_GENDER,
              name = SELECTED_NAME,
              nameUrl = SELECTED_NAME_URL,
              biography = SELECTED_BIOGRAPHY,
              idTmdb = SELECTED_ID_TMDB,
              idImdb = SELECTED_ID_IMDB,
              idTwitter = SELECTED_ID_TWITTER,
              idInstagram = SELECTED_ID_INSTAGRAM,
              imagePoster = SELECTED_IMAGE_POSTER,
              adult = SELECTED_ADULT,
              visibility = SELECTED_VISIBILITY,
              birthPlace = SELECTED_BIRTH_PLACE,
              birthDate = SELECTED_BIRTH_DATE,
              deathDate = SELECTED_DEATH_DATE,
              lastEditDate = SELECTED_LAST_EDIT_DATE,
            ))
            db.session.commit()
        except:
            db.session.rollback()

  class Movie:
    def addContent(get_tmdb_id):
      #if not check_admin(): return 1

      SELECTED_ID_ADD_PROFILE = session['PROFILE']['idProfile']
      SELECTED_ID_ADD_ACCOUNT = session['ACCOUNT']['idAccount']
      SELECTED_TYPE = 'MOVIE'
      SELECTED_TITLE = '#'
      SELECTED_TITLE_ORIGINAL = '#'
      SELECTED_TITLE_URL = '#'
      SELECTED_OVERVIEW = '#'
      SELECTED_ID_TMDB = get_tmdb_id
      SELECTED_ID_IMDB = '#'
      SELECTED_IMAGE_POSTER = '/static/img/defaults/poster_content.png'
      SELECTED_IMAGE_BACKGROUND = '/static/img/defaults/background_content.png'
      SELECTED_ADULT = 0
      SELECTED_VISIBILITY = 1
      SELECTED_VOTE_AVERAGE = 0
      SELECTED_RELEASE_DATE = '#'
      SELECTED_LAST_EDIT_DATE = datetime.now(pytz.timezone(PY_TIMEZONE))

      get_details = tmdb.Movies(get_tmdb_id).info(language=TMDB_LANGUAGE)
      get_external_ids = tmdb.Movies(get_tmdb_id).external_ids(language=TMDB_LANGUAGE)

      if get_details['title'] != None: SELECTED_TITLE = get_details['title']
      if get_details['original_title'] != None:
        SELECTED_TITLE_ORIGINAL = get_details['original_title']
        #SELECTED_TITLE_URL = get_details['original_title'].lower().replace(' ', '-').replace('.', '').replace(':', '').replace("'", '')
        SELECTED_TITLE_URL = slugify(get_details['original_title'])
        if content.query.filter(and_(content.titleUrl == SELECTED_TITLE_URL, content.type == 'MOVIE')).first() != None: SELECTED_TITLE_URL = SELECTED_TITLE_URL + '_' + id_generator(size=4)
      if get_details['overview'] != None: SELECTED_OVERVIEW = get_details['overview']
      if get_details['id'] != None: SELECTED_ID_TMDB = get_details['id']
      ### external ids
      if get_external_ids['imdb_id'] != None: SELECTED_ID_IMDB = get_external_ids['imdb_id']
      ### end external ids
      if get_details['poster_path'] != None: SELECTED_IMAGE_POSTER = 'https://www.themoviedb.org/t/p/w300' + get_details['poster_path']
      if get_details['backdrop_path'] != None: SELECTED_IMAGE_BACKGROUND = 'https://www.themoviedb.org/t/p/w500' + get_details['backdrop_path']
      if get_details['adult'] != None:
        #SELECTED_ADULT = get_details['adult']
        if get_details['adult']: SELECTED_ADULT = 1
      if get_details['vote_average'] != None: SELECTED_VOTE_AVERAGE = get_details['vote_average']
      if get_details['release_date'] != None: SELECTED_RELEASE_DATE = get_details['release_date']

      if content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == str(SELECTED_TYPE))).first() != None: pass
      else:
        try:
            db.session.add(content(
              idAddProfile = SELECTED_ID_ADD_PROFILE,
              idAddAccount = SELECTED_ID_ADD_ACCOUNT,
              type = SELECTED_TYPE,
              title = SELECTED_TITLE,
              titleOriginal = SELECTED_TITLE_ORIGINAL,
              titleUrl = SELECTED_TITLE_URL,
              overview = SELECTED_OVERVIEW,
              idTmdb = SELECTED_ID_TMDB,
              idImdb = SELECTED_ID_IMDB,
              imagePoster = SELECTED_IMAGE_POSTER,
              imageBackground = SELECTED_IMAGE_BACKGROUND,
              adult = SELECTED_ADULT,
              visibility = SELECTED_VISIBILITY,
              voteAverage = SELECTED_VOTE_AVERAGE,
              releaseDate = SELECTED_RELEASE_DATE,
              lastEditDate = SELECTED_LAST_EDIT_DATE,
            ))
            db.session.commit()
        except:
            db.session.rollback()

      for get_genre in get_details['genres']:
        if movieContentGenre.query.filter(and_(movieContentGenre.idContent == str(content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent), movieContentGenre.idGenre == str(get_genre['id']))).first() != None: pass
        else:
          try:
              db.session.add(movieContentGenre(
                idContent = content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent,
                idGenre = get_genre['id']
              ))
              db.session.commit()
          except:
              db.session.rollback()

      for get_language in get_details['spoken_languages']:
        if contentLanguage.query.filter(and_(contentLanguage.idContent == str(content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent), contentLanguage.idISO_639_1 == str(get_language['iso_639_1']))).first() != None: pass
        else:
          try:
              db.session.add(contentLanguage(
                idContent = content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent,
                idISO_639_1 = get_language['iso_639_1']
              ))
              db.session.commit()
          except:
              db.session.rollback()

      for get_country in get_details['production_countries']:
        if contentCountry.query.filter(and_(contentCountry.idContent == str(content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent), contentCountry.idISO_3166_1 == str(get_country['iso_3166_1']))).first() != None: pass
        else:
          try:
              db.session.add(contentCountry(
                idContent = content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent,
                idISO_3166_1 = get_country['iso_3166_1']
              ))
              db.session.commit()
          except:
              db.session.rollback()

    # BETA TAG BEGIN
    def addTag(get_tmdb_id):
      #if not check_admin(): return 1

      get_content = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first()
      if get_content:
        get_title = get_content.title.lower()
        get_original_title = get_content.titleOriginal.lower()
        get_release_year = get_content.releaseDate[:4]

        tag_list = []
        tag_list.append('{} {} izle'.format(get_title, get_release_year))
        tag_list.append('{} {} izle'.format(get_original_title, get_release_year))

        tag_list.append('{} {} türkçe dublaj izle'.format(get_title, get_release_year))
        tag_list.append('{} {} türkçe altyazı izle'.format(get_title, get_release_year))

        tag_list.append('{} {} türkçe dublaj izle'.format(get_original_title, get_release_year))
        tag_list.append('{} {} türkçe altyazı izle'.format(get_original_title, get_release_year))

        for _tag in tag_list:
          if not contentTag.query.filter(and_(contentTag.idContent == get_content.idContent, contentTag.title == _tag)).first():
            try:
                db.session.add(contentTag(
                  idContent = get_content.idContent,
                  title = _tag,
                ))
                db.session.commit()
            except:
                db.session.rollback()
    # BETA TAG END 

    def addTrailer(get_tmdb_id):
      #if not check_admin(): return 1

      # check if content exists
      if content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first():
        # first check local trailers, if there are uploaded trailer for the selected movie then get the first one
        get_local_trailers = tmdb.Movies(get_tmdb_id).videos(language=TMDB_LANGUAGE)['results']
        if len(get_local_trailers) >= 1:
          for local_trailer in get_local_trailers:
            if local_trailer['type'] == 'Trailer' and local_trailer['site'] == 'YouTube':
              # check if already added
              if not moviePlayer.query.filter(moviePlayer.source == 'https://www.youtube.com/embed/' + str(local_trailer['key'])).first():
                try:
                  db.session.add(moviePlayer(
                    idContent = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first().idContent,
                    idAddProfile = session['PROFILE']['idProfile'],
                    idAddAccount = session['ACCOUNT']['idAccount'],
                    language = 'DUBBED',
                    source = 'https://www.youtube.com/embed/' + str(local_trailer['key']),
                    title = str(local_trailer['name']),
                    type = 'TRAILER',
                    visibility = 1,
                    order = 0,
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
                  ))
                  db.session.commit()
                except:
                  db.session.rollback()
                break
        # else check global trailers, and add the first one
        else:
          get_global_trailers = tmdb.Movies(get_tmdb_id).videos()['results']
          if len(get_global_trailers) >= 1:
            for global_trailer in get_global_trailers:
              if global_trailer['type'] == 'Trailer' and global_trailer['site'] == 'YouTube':
                # check if already added
                if not moviePlayer.query.filter(moviePlayer.source == 'https://www.youtube.com/embed/' + str(global_trailer['key'])).first():
                  try:
                    db.session.add(moviePlayer(
                      idContent = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first().idContent,
                      idAddProfile = session['PROFILE']['idProfile'],
                      idAddAccount = session['ACCOUNT']['idAccount'],
                      language = 'ORIGINAL',
                      source = 'https://www.youtube.com/embed/' + str(global_trailer['key']),
                      title = str(global_trailer['name']),
                      type = 'TRAILER',
                      visibility = 1,
                      order = 0,
                      lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
                    ))
                    db.session.commit()
                  except:
                    db.session.rollback()
                  break

    def addPlayer(get_tmdb_id):
      #if not check_admin(): return 1

      if content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first() == None: pass
      else:
        if moviePlayer.query.filter_by(source=soup_global_beta.get_movie_player_src(get_tmdb_id)).first() != None: pass
        else:
          try:
              db.session.add(moviePlayer(
                idContent = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first().idContent,
                idAddProfile = session['PROFILE']['idProfile'],
                idAddAccount = session['ACCOUNT']['idAccount'],
                language = 'ORIGINAL',
                source = soup_global_beta.get_movie_player_src(get_tmdb_id),
                title = '2emb.global',
                type = 'IFRAME',
                visibility = 1,
                order = 1,
                lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
              ))
              db.session.commit()
          except:
              db.session.rollback()

      ### BETA SOUP LOCAL BEGIN
      # ONLY FOR MOVIES THO #
      """
      try:
        get_tmdb_details = tmdb.Movies(get_tmdb_id).info()
        get_local_player = Soup_Local(query=str(get_tmdb_details['original_title']) + ' ' + str(get_tmdb_details['release_date'][:4]))
        if moviePlayer.query.filter_by(source=get_local_player.get_movie_player_src(get_url=get_local_player.get_first_item_href(get_query=get_local_player.query))).first() != None: pass
        else:
          db.session.add(moviePlayer(
            idContent = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first().idContent,
            idAddProfile = session['PROFILE']['idProfile'],
            idAddAccount = session['ACCOUNT']['idAccount'],
            language = 'DUBBED',
            source = get_local_player.get_movie_player_src(get_url=get_local_player.get_first_item_href(get_query=get_local_player.query)),
            title = 'WG.Local',
            type = 'IFRAME',
            visibility = True,
            order = 1,
            lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
          ))
          db.session.commit()
      except: print('SOUP LOCAL EXCEPT!')
      """
      ### BETA SOUP LOCAL END

    """
    comprehensive
    =============
    uses addContent, addPlayer
    and addCast at the same time
    """
    def addComprehensive_stable_with_cast_limit(get_tmdb_id):
      try:
        DEF_MAX_CAST_RANGE = 20

        TMDBSimpleasy.Movie.addContent(get_tmdb_id=get_tmdb_id)
        TMDBSimpleasy.Movie.addTag(get_tmdb_id=get_tmdb_id)
        get_casts = tmdb.Movies(get_tmdb_id).credits(language=TMDB_LANGUAGE)['cast']

        for loop_cast in range(DEF_MAX_CAST_RANGE):
          if loop_cast < len(get_casts):

            TMDBSimpleasy.Cast.addCast(get_casts[loop_cast]['id'])
            if contentCast.query.filter(and_(contentCast.idContent == str(content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first().idContent), contentCast.idCast == str(cast.query.filter_by(idTmdb=str(get_casts[loop_cast]['id'])).first().idCast))).first() != None: pass
            else:
              try:
                  db.session.add(contentCast(
                    idContent = content.query.filter(and_(content.idTmdb == get_tmdb_id, content.type == 'MOVIE')).first().idContent,
                    idCast = cast.query.filter_by(idTmdb=str(get_casts[loop_cast]['id'])).first().idCast,
                    character = get_casts[loop_cast]['character'],
                    order = get_casts[loop_cast]['order'],
                  ))

                  db.session.commit()
              except:
                  db.session.rollback()
        TMDBSimpleasy.Movie.addTrailer(get_tmdb_id=get_tmdb_id)
        TMDBSimpleasy.Movie.addPlayer(get_tmdb_id=get_tmdb_id)
      except Exception as e: print('ERROR COMPREHENSIVE :::: {}'.format(e))

    ### TESTED FEW TIMES, it seems like it works quite well 
    def addComprehensive(get_tmdb_id):
        try:
            TMDBSimpleasy.Movie.addContent(get_tmdb_id=get_tmdb_id)
            TMDBSimpleasy.Movie.addTag(get_tmdb_id=get_tmdb_id)
            try:
                get_casts = tmdb.Movies(get_tmdb_id).credits(language=TMDB_LANGUAGE)['cast']
                for get_cast in get_casts:
                    TMDBSimpleasy.Cast.addCast(get_cast['id'])
                    if contentCast.query.filter(and_(contentCast.idContent == str(content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'MOVIE')).first().idContent), contentCast.idCast == str(cast.query.filter_by(idTmdb=str(get_cast['id'])).first().idCast))).first() != None: pass
                    else:
                        try:
                            db.session.add(contentCast(
                                idContent = content.query.filter(and_(content.idTmdb == get_tmdb_id, content.type == 'MOVIE')).first().idContent,
                                idCast = cast.query.filter_by(idTmdb=str(get_cast['id'])).first().idCast,
                                character = get_cast['character'],
                                order = get_cast['order'],
                            ))

                            db.session.commit()
                        except:
                            db.session.rollback()
            except Exception as e: print(' ======> EXCEPTION: {}'.format(e)) 
            try:
                TMDBSimpleasy.Movie.addTrailer(get_tmdb_id=get_tmdb_id)
                TMDBSimpleasy.Movie.addPlayer(get_tmdb_id=get_tmdb_id)
            except Exception as e: print(' ======> EXCEPTION: {}'.format(e)) 
        except Exception as e: print('ERROR COMPREHENSIVE :::: {}'.format(e))

  class TV:
    def addContent(get_tmdb_id):
      #if not check_admin(): return 1

      SELECTED_ID_ADD_PROFILE = session['PROFILE']['idProfile']
      SELECTED_ID_ADD_ACCOUNT = session['ACCOUNT']['idAccount']
      SELECTED_TYPE = 'TV'
      SELECTED_TITLE = '#'
      SELECTED_TITLE_ORIGINAL = '#'
      SELECTED_TITLE_URL = '#'
      SELECTED_OVERVIEW = '#'
      SELECTED_ID_TMDB = get_tmdb_id
      SELECTED_ID_IMDB = '#'
      SELECTED_IMAGE_POSTER = '/static/img/defaults/poster_content.png'
      SELECTED_IMAGE_BACKGROUND = '/static/img/defaults/background_content.png'
      SELECTED_ADULT = 0
      SELECTED_VISIBILITY = 1
      SELECTED_VOTE_AVERAGE = 0
      SELECTED_RELEASE_DATE = '#'
      SELECTED_LAST_EDIT_DATE = datetime.now(pytz.timezone(PY_TIMEZONE))

      get_details = tmdb.TV(get_tmdb_id).info(language=TMDB_LANGUAGE)
      get_external_ids = tmdb.TV(get_tmdb_id).external_ids(language=TMDB_LANGUAGE)

      if get_details['name'] != None: SELECTED_TITLE = get_details['name']
      if get_details['original_name'] != None:
        SELECTED_TITLE_ORIGINAL = get_details['original_name']
        #SELECTED_TITLE_URL = get_details['original_name'].lower().replace(' ', '-').replace('.', '').replace(':', '').replace("'", '')
        SELECTED_TITLE_URL = slugify(get_details['original_name'])
        if content.query.filter(and_(content.titleUrl == SELECTED_TITLE_URL, content.type == 'TV')).first() != None: SELECTED_TITLE_URL = SELECTED_TITLE_URL + '_' + id_generator(size=4)
      if get_details['overview'] != None: SELECTED_OVERVIEW = get_details['overview']
      if get_details['id'] != None: SELECTED_ID_TMDB = get_details['id']
      ### external ids
      if get_external_ids['imdb_id'] != None: SELECTED_ID_IMDB = get_external_ids['imdb_id']
      ### end external ids
      if get_details['poster_path'] != None: SELECTED_IMAGE_POSTER = 'https://www.themoviedb.org/t/p/w300' + get_details['poster_path']
      if get_details['backdrop_path'] != None: SELECTED_IMAGE_BACKGROUND = 'https://www.themoviedb.org/t/p/w500' + get_details['backdrop_path']
      if get_details['vote_average'] != None: SELECTED_VOTE_AVERAGE = get_details['vote_average']
      if get_details['first_air_date'] != None: SELECTED_RELEASE_DATE = get_details['first_air_date']

      if content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first() != None: pass
      else:
        try:
            db.session.add(content(
              idAddProfile = SELECTED_ID_ADD_PROFILE,
              idAddAccount = SELECTED_ID_ADD_ACCOUNT,
              type = SELECTED_TYPE,
              title = SELECTED_TITLE,
              titleOriginal = SELECTED_TITLE_ORIGINAL,
              titleUrl = SELECTED_TITLE_URL,
              overview = SELECTED_OVERVIEW,
              idTmdb = SELECTED_ID_TMDB,
              idImdb = SELECTED_ID_IMDB,
              imagePoster = SELECTED_IMAGE_POSTER,
              imageBackground = SELECTED_IMAGE_BACKGROUND,
              adult = SELECTED_ADULT,
              visibility = SELECTED_VISIBILITY,
              voteAverage = SELECTED_VOTE_AVERAGE,
              releaseDate = SELECTED_RELEASE_DATE,
              lastEditDate = SELECTED_LAST_EDIT_DATE,
            ))
            db.session.commit()
        except:
            db.session.rollback()

      for get_genre in get_details['genres']:
        if tvContentGenre.query.filter(and_(tvContentGenre.idContent == str(content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent), tvContentGenre.idGenre == str(get_genre['id']))).first() != None: pass
        else:
            try:
              db.session.add(tvContentGenre(
                idContent = content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent,
                idGenre = get_genre['id']
              ))
              db.session.commit()
            except:
              db.session.rollback()

      for get_language in get_details['spoken_languages']:
        if contentLanguage.query.filter(and_(contentLanguage.idContent == str(content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent), contentLanguage.idISO_639_1 == str(get_language['iso_639_1']))).first() != None: pass
        else:
            try:
              db.session.add(contentLanguage(
                idContent = content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent,
                idISO_639_1 = get_language['iso_639_1']
              ))
              db.session.commit()
            except:
              db.session.rollback()

      for get_country in get_details['production_countries']:
        if contentCountry.query.filter(and_(contentCountry.idContent == str(content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent), contentCountry.idISO_3166_1 == str(get_country['iso_3166_1']))).first() != None: pass
        else:
            try:
              db.session.add(contentCountry(
                idContent = content.query.filter(and_(content.idTmdb == str(SELECTED_ID_TMDB), content.type == SELECTED_TYPE)).first().idContent,
                idISO_3166_1 = get_country['iso_3166_1']
              ))
              db.session.commit()
            except:
              db.session.rollback()

    def addTag(get_tmdb_id):
      #if not check_admin(): return 1

      get_content = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'TV')).first()
      if get_content:
        get_title = get_content.title.lower()
        get_original_title = get_content.titleOriginal.lower()
        get_release_year = get_content.releaseDate[:4]

        tag_list = []
        tag_list.append('{} {} izle'.format(get_title, get_release_year))
        tag_list.append('{} {} izle'.format(get_original_title, get_release_year))

        tag_list.append('{} {} türkçe dublaj izle'.format(get_title, get_release_year))
        tag_list.append('{} {} türkçe altyazı izle'.format(get_title, get_release_year))

        tag_list.append('{} {} türkçe dublaj izle'.format(get_original_title, get_release_year))
        tag_list.append('{} {} türkçe altyazı izle'.format(get_original_title, get_release_year))

        for _tag in tag_list:
          if not contentTag.query.filter(and_(contentTag.idContent == get_content.idContent, contentTag.title == _tag)).first():
            try:
              db.session.add(contentTag(
                idContent = get_content.idContent,
                title = _tag,
              ))
              db.session.commit()
            except:
              db.session.rollback()

    def addSeason(get_tmdb_id, get_season_number):
      #if not check_admin(): return 1

      SELECTED_ID_CONTENT = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'TV')).first().idContent
      SELECTED_ID_ADD_PROFILE = session['PROFILE']['idProfile']
      SELECTED_ID_ADD_ACCOUNT = session['ACCOUNT']['idAccount']
      SELECTED_TITLE = '#'
      SELECTED_OVERVIEW = '#'
      SELECTED_ID_TMDB = get_tmdb_id
      SELECTED_IMAGE_POSTER = '/static/img/defaults/poster_season.png'
      SELECTED_SEASON_NUMBER = get_season_number
      SELECTED_VISIBILITY = 1 
      SELECTED_AIR_DATE = '#'
      SELECTED_LAST_EDIT_DATE = datetime.now(pytz.timezone(PY_TIMEZONE))

      get_details = tmdb.TV_Seasons(SELECTED_ID_TMDB, SELECTED_SEASON_NUMBER).info(language=TMDB_LANGUAGE)

      if get_details['name'] != None: SELECTED_TITLE = get_details['name']
      if get_details['overview'] != None: SELECTED_OVERVIEW = get_details['overview']
      if get_details['poster_path'] != None: SELECTED_IMAGE_POSTER = 'https://www.themoviedb.org/t/p/w300' + get_details['poster_path']
      if get_details['air_date'] != None: SELECTED_AIR_DATE = get_details['air_date']

      if tvSeasonContent.query.filter(and_(tvSeasonContent.idTmdb == str(SELECTED_ID_TMDB), tvSeasonContent.seasonNumber == SELECTED_SEASON_NUMBER)).first() != None: pass
      else:
        try:
            db.session.add(tvSeasonContent(
              idContent = SELECTED_ID_CONTENT,
              idAddProfile = SELECTED_ID_ADD_PROFILE,
              idAddAccount = SELECTED_ID_ADD_ACCOUNT,
              title = SELECTED_TITLE,
              overview = SELECTED_OVERVIEW,
              idTmdb = SELECTED_ID_TMDB,
              imagePoster = SELECTED_IMAGE_POSTER,
              seasonNumber = SELECTED_SEASON_NUMBER,
              visibility = SELECTED_VISIBILITY,
              airDate = SELECTED_AIR_DATE,
              lastEditDate = SELECTED_LAST_EDIT_DATE,
            ))
            db.session.commit()
        except:
            db.session.rollback()

    def addEpisode(get_tmdb_id, get_season_number, get_episode_number):
      #if not check_admin(): return 1

      SELECTED_ID_TV_SEASON = tvSeasonContent.query.filter(and_(tvSeasonContent.idTmdb == str(get_tmdb_id), tvSeasonContent.seasonNumber == get_season_number)).first().idTvSeason
      SELECTED_ID_CONTENT = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'TV')).first().idContent
      SELECTED_ID_ADD_PROFILE = session['PROFILE']['idProfile']
      SELECTED_ID_ADD_ACCOUNT = session['ACCOUNT']['idAccount']
      SELECTED_TITLE = '#'
      SELECTED_OVERVIEW = '#'
      SELECTED_ID_TMDB = get_tmdb_id
      SELECTED_ID_IMDB = '#'
      SELECTED_IMAGE_POSTER = '/static/img/defaults/poster_episode.png'
      SELECTED_SEASON_NUMBER = get_season_number
      SELECTED_EPISODE_NUMBER = get_episode_number
      SELECTED_VISIBILITY = 1 
      SELECTED_VOTE_AVERAGE = 0
      SELECTED_AIR_DATE = '#'
      SELECTED_LAST_EDIT_DATE = datetime.now(pytz.timezone(PY_TIMEZONE))

      get_details = tmdb.TV_Episodes(SELECTED_ID_TMDB, SELECTED_SEASON_NUMBER, SELECTED_EPISODE_NUMBER).info(language=TMDB_LANGUAGE)
      get_external_ids = tmdb.TV_Episodes(SELECTED_ID_TMDB, SELECTED_SEASON_NUMBER, SELECTED_EPISODE_NUMBER).external_ids(language=TMDB_LANGUAGE)

      if get_details['name'] != None: SELECTED_TITLE = get_details['name']
      if get_details['overview'] != None: SELECTED_OVERVIEW = get_details['overview']
      ### external ids
      if get_external_ids['imdb_id'] != None: SELECTED_ID_IMDB = get_external_ids['imdb_id']
      ### end external ids
      if get_details['still_path'] != None: SELECTED_IMAGE_POSTER = 'https://www.themoviedb.org/t/p/w500' + get_details['still_path']
      if get_details['vote_average'] != None: SELECTED_VOTE_AVERAGE = get_details['vote_average']
      if get_details['air_date'] != None: SELECTED_AIR_DATE = get_details['air_date']

      if tvEpisodeContent.query.filter(and_(tvEpisodeContent.idTmdb == str(SELECTED_ID_TMDB), tvEpisodeContent.seasonNumber == SELECTED_SEASON_NUMBER, tvEpisodeContent.episodeNumber == SELECTED_EPISODE_NUMBER)).first() != None: pass
      else:
        try:
            db.session.add(tvEpisodeContent(
              idTvSeason = SELECTED_ID_TV_SEASON,
              idContent = SELECTED_ID_CONTENT,
              idAddProfile = SELECTED_ID_ADD_PROFILE,
              idAddAccount = SELECTED_ID_ADD_ACCOUNT,
              title = SELECTED_TITLE,
              overview = SELECTED_OVERVIEW,
              idTmdb = SELECTED_ID_TMDB,
              idImdb = SELECTED_ID_IMDB,
              imagePoster = SELECTED_IMAGE_POSTER,
              seasonNumber = SELECTED_SEASON_NUMBER,
              episodeNumber = SELECTED_EPISODE_NUMBER,
              visibility = SELECTED_VISIBILITY,
              voteAverage = SELECTED_VOTE_AVERAGE,
              airDate = SELECTED_AIR_DATE,
              lastEditDate = SELECTED_LAST_EDIT_DATE,
            ))
            db.session.commit()
        except:
            db.session.rollback()

    def addPlayer(get_tmdb_id, get_season_number, get_episode_number):
      #if not check_admin(): return 1

      if content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'TV')).first() == None: pass
      else:
        if tvPlayer.query.filter_by(source=soup_global_beta.get_tv_player_src(get_tmdb_id, get_season_number, get_episode_number)).first() != None: pass
        else:
            try:
              db.session.add(tvPlayer(
                idTvSeason = tvSeasonContent.query.filter(and_(tvSeasonContent.idTmdb == str(get_tmdb_id), tvSeasonContent.seasonNumber == get_season_number)).first().idTvSeason,
                idTvEpisode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idTmdb == str(get_tmdb_id), tvEpisodeContent.seasonNumber == get_season_number, tvEpisodeContent.episodeNumber == get_episode_number)).first().idTvEpisode,
                idContent = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'TV')).first().idContent,
                idAddProfile = session['PROFILE']['idProfile'],
                idAddAccount = session['ACCOUNT']['idAccount'],
                language = 'ORIGINAL',
                source = soup_global_beta.get_tv_player_src(get_tmdb_id, get_season_number, get_episode_number),
                title = '2emb.global',
                type = 'IFRAME',
                seasonNumber = get_season_number,
                episodeNumber = get_episode_number,
                visibility = 1,
                order = 1,
                lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
              ))
              db.session.commit()
            except:
              db.session.rollback()

    """
    comprehensive
    =============
    uses addContent, addPlayer,
    addSeason, addEpisode,
    and addCast at the same time
    """
    def addComprehensive(get_tmdb_id):
        try:
            TMDBSimpleasy.TV.addContent(get_tmdb_id=get_tmdb_id)
            TMDBSimpleasy.TV.addTag(get_tmdb_id=get_tmdb_id)
            try:
                get_casts = tmdb.TV(get_tmdb_id).credits(language=TMDB_LANGUAGE)['cast']
                for get_cast in get_casts:
                    TMDBSimpleasy.Cast.addCast(get_cast['id'])
                    if contentCast.query.filter(and_(contentCast.idContent == str(content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'TV')).first().idContent), contentCast.idCast == str(cast.query.filter_by(idTmdb=str(get_cast['id'])).first().idCast))).first() != None: pass
                    else:
                        try:
                            db.session.add(contentCast(
                                idContent = content.query.filter(and_(content.idTmdb == str(get_tmdb_id), content.type == 'TV')).first().idContent,
                                idCast = cast.query.filter_by(idTmdb=str(get_cast['id'])).first().idCast,
                                character = get_cast['character'],
                                order = get_cast['order'],
                            ))

                            db.session.commit()
                        except:
                            db.session.rollback()
            except Exception as e: print(' ======> EXCEPTION: {}'.format(e)) 
            try:
                for get_season in tmdb.TV(get_tmdb_id).info(language=TMDB_LANGUAGE)['seasons']:
                    TMDBSimpleasy.TV.addSeason(get_tmdb_id=get_tmdb_id, get_season_number=get_season['season_number'])
                    for get_episode in tmdb.TV_Seasons(get_tmdb_id, get_season['season_number']).info(language=TMDB_LANGUAGE)['episodes']:
                        TMDBSimpleasy.TV.addEpisode(get_tmdb_id=get_tmdb_id, get_season_number=get_season['season_number'], get_episode_number=get_episode['episode_number'])
                        TMDBSimpleasy.TV.addPlayer(get_tmdb_id=get_tmdb_id, get_season_number=get_season['season_number'], get_episode_number=get_episode['episode_number'])
                        time.sleep(2) # JUST TESTING SOMETHING
            except Exception as e: print(' ======> EXCEPTION: {}'.format(e)) 
        except Exception as e: print(' ======> EXCEPTION: {}'.format(e)) 
