# -*- encoding: utf-8 -*-
from includes import *

"""
ajax codes for only admins 
"""

###########################
###### highlights 
###########################
@app.route('/adminproc/highlights', methods=['POST'])
def adminproc_highlights():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  if get_function == 'addOrDrop':
    content_input = request.get_json()['inputContent'] # it's called `inputContent` because it can be idContent, title, titleOriginal or titleUrl
    if not content_input: return make_response(jsonify({'err_msg': '`content_input` boş bırakıldı.'}))

    get_content = content.query.filter(or_(content.idContent == content_input, content.title.like('%{}%'.format(content_input)), content.titleOriginal.like('%{}%'.format(content_input)), content.titleUrl.like('%{}%'.format(content_input)))).first()
    if not get_content: return make_response(jsonify({'err_msg': '`content->query` boş bırakıldı.'}))

    get_highlight_content = highlightContent.query.filter(highlightContent.idContent == get_content.idContent).first()

    if get_highlight_content:
      get_highlight_content.drop()
      return make_response(jsonify({'succ_msg': 'Öne çıkarılanlardan başarıyla kaldırıldı!'}))
    else:
      db.session.add(highlightContent(
        idContent = get_content.idContent,
        idAddProfile = get_logged_profile().idProfile,
        idAddAccount = get_logged_account().idAccount
      ))
      db.session.commit()
      return make_response(jsonify({'succ_msg': 'Öne çıkarılanlara başarıyla eklendi!'}))
###########################
###### end highlights
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

###########################
###### contents 
###########################
@app.route('/adminproc/contents', methods=['POST'])
def adminproc_contents():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # VISIBILITY SWITCH
  if get_function == 'visibilitySwitch':
    content_id = request.get_json()['idContent']
    if not content_id: return make_response(jsonify({'err_msg': '`content_id` boş bırakıldı.'}))

    get_content = content.query.filter(content.idContent == content_id).first()
    if not get_content: return make_response(jsonify({'err_msg': '`content->query` boş bırakıldı.'}))

    if get_content.visibility == 1: get_content.visibility = 0
    elif get_content.visibility == 0: get_content.visibility = 1

    db.session.commit()
    return make_response(jsonify({'succ_msg': 'Görünürlük başarıyla değiştirildi!'}))

  # DROP
  if get_function == 'drop':
    content_id = request.get_json()['idContent']
    if not content_id: return make_response(jsonify({'err_msg': '`content_id` boş bırakıldı.'}))

    get_content = content.query.filter(content.idContent == content_id).first()
    if not get_content: return make_response(jsonify({'err_msg': '`content->query` boş bırakıldı.'}))

    get_content.drop()

    return make_response(jsonify({'succ_msg': 'İçerik başarıyla silindi!'}))

  # TMDB IMPORT
  if get_function == 'tmdbImport':
    content_type = request.get_json()['type']
    tmdb_id = request.get_json()['idTmdb'] 

    if content_type == 'MOVIE':
      check_content = content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'MOVIE')).first()
      if check_content: return make_response(jsonify({'err_msg': '`content->query` dolu değerli.'}))

      try:
        TMDBSimpleasy.Movie.addComprehensive(get_tmdb_id=tmdb_id)
        return make_response(jsonify({'ret_url': url_for('adminpanel_content_edit', title_url=content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'MOVIE')).first().titleUrl)}))
      except Exception as e: return make_response(jsonify({'err_msg': '{}'.format(e)}))

    elif content_type == 'TV':
      check_content = content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'TV')).first()
      if check_content: return make_response(jsonify({'err_msg': '`content->query` dolu değerli.'}))

      try:
        TMDBSimpleasy.TV.addComprehensive(get_tmdb_id=tmdb_id)
        return make_response(jsonify({'ret_url', url_for('adminpanel_content_edit', title_url=content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'TV')).first().titleUrl)}))
      except Exception as e: return make_response(jsonify({'err_msg': '{}'.format(e)}))

  # CREATE NATURAL
  if get_function == 'createNatural':
    content_type = request.get_json()['type']
    
    if content_type == 'MOVIE' or content_type == 'TV':
      def_random_id = id_generator(chars=string.digits, size=8)

      db.session.add(content(
        idAddProfile = get_logged_profile().idProfile,
        idAddAccount = get_logged_account().idAccount,
        type = content_type,
        title = 'İçerik {}'.format(def_random_id),
        titleOriginal = 'Content {}'.format(def_random_id),
        titleUrl = 'content-{}'.format(def_random_id),
        overview = '#',
        idTmdb = '#',
        idImdb = '#',
        imagePoster = '/static/img/defaults/poster_content.png',
        imageBackground = '/static/img/defaults/background_content.png',
        adult = 0,
        visibility = 1,
        voteAverage = 0,
        releaseDate = str(datetime.now()),
        lastEditDate = str(datetime.now()),
      ))
      db.session.commit()

      return make_response(jsonify({'ret_url': url_for('adminpanel_content_edit', title_url='content-{}'.format(def_random_id))}))
###########################
###### end contents 
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

###########################
###### content->players
###########################
@app.route('/adminproc/content/players', methods=['POST'])
def adminproc_content_players():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    player_id = request.get_json()['idPlayer']
    if not player_id: return make_response(jsonify({'err_msg': '`player_id` boş bırakıldı.'}))

    get_player = moviePlayer.query.filter(moviePlayer.idPlayer == player_id).first()
    if not get_player: return make_response(jsonify({'err_msg': '`moviePlayer->query` boş bırakıldı.'}))

    get_player.drop()

    return make_response(jsonify({'succ_msg': 'Oynatıcı başarıyla silindi!'}))

  # TMDB IMPORT
  if get_function == 'tmdbImport':
    tmdb_id = request.get_json()['idTmdb'] 

    check_content = content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'MOVIE')).first()
    if not check_content: return make_response(jsonify({'err_msg': '`content->query` boş bırakıldı.'}))

    try:
      TMDBSimpleasy.Movie.addPlayer(get_tmdb_id=tmdb_id)

      return make_response(jsonify({'ret_url', url_for('adminpanel_content_players', title_url=check_content.titleUrl)}))
    except Exception as e: return make_response(jsonify({'err_msg': '{}'.format(e)}))

  # CREATE NATURAL
  if get_function == 'createNatural':
    content_id = request.get_json()['idContent']
    if not content_id: pass

    def_random_id = id_generator(chars=string.digits, size=5)

    db.session.add(moviePlayer(
      idContent = content_id, 
      idAddProfile = get_logged_profile().idProfile,
      idAddAccount = get_logged_account().idAccount,
      language = 'ORIGINAL',
      source = '#',
      title = 'İçerik {}'.format(def_random_id),
      type = 'PLYR',
      visibility = 1,
      order = 1,
      lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
    ))

    db.session.commit()

    return make_response(jsonify({'ret_url': url_for('adminpanel_content_player_edit', title_url=content.query.filter(and_(content.idContent == content_id, content.type == 'MOVIE')).first().titleUrl, view_key=moviePlayer.query.filter(moviePlayer.title == 'İçerik {}'.format(def_random_id)).first().viewKey)}))
###########################
###### end content->players
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

###########################
###### content->seasons
###########################
@app.route('/adminproc/content/seasons', methods=['POST'])
def adminproc_content_seasons():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    season_id = request.get_json()['idTvSeason']
    if not season_id: return make_response(jsonify({'err_msg': '`season_id` boş bırakıldı.'}))

    get_season = tvSeasonContent.query.filter(tvSeasonContent.idTvSeason == season_id).first()
    if not get_season: return make_response(jsonify({'err_msg': '`tvSeasonContent->query` boş bırakıldı.'}))

    get_season.drop()

    return make_response(jsonify({'succ_msg': 'Sezon başarıyla silindi!'}))

  # TMDB IMPORT
  if get_function == 'tmdbImport':
    tmdb_id = request.get_json()['idTmdb'] 
    season_number = request.get_json()['seasonNumber']

    check_content = content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'TV')).first()
    if not check_content: return make_response(jsonify({'err_msg': '`content->query` boş bırakıldı.'}))

    try:
      TMDBSimpleasy.TV.addSeason(get_tmdb_id=tmdb_id, get_season_number=season_number)
      for get_episode in tmdb.TV_Seasons(tmdb_id, season_number).info(language=TMDB_LANGUAGE)['episodes']:
        TMDBSimpleasy.TV.addEpisode(get_tmdb_id=tmdb_id, get_season_number=season_number, get_episode_number=get_episode['episode_number'])
        TMDBSimpleasy.TV.addPlayer(get_tmdb_id=tmdb_id, get_season_number=season_number, get_episode_number=get_episode['episode_number'])

      return make_response(jsonify({'ret_url', url_for('adminpanel_content_seasons', title_url=check_content.titleUrl)}))
    except Exception as e: return make_response(jsonify({'err_msg': '{}'.format(e)}))

  # CREATE NATURAL
  if get_function == 'createNatural':
    content_id = request.get_json()['idContent']
    if not content_id: pass

    def_random_id = id_generator(chars=string.digits, size=5)
    def_random_season_number = randint(125125, 912859125)

    db.session.add(tvSeasonContent(
      #idContent = content.query.filter(and_(content.idContent == content_id, content.type == 'TV')).first().idContent,
      idContent = content_id,
      idAddProfile = get_logged_profile().idProfile,
      idAddAccount = get_logged_account().idAccount,
      title = 'İçerik {}'.format(def_random_id),
      overview = '#',
      idTmdb = '#',
      imagePoster = '/static/img/defaults/poster_season.png',
      seasonNumber = def_random_season_number,
      visibility = 1,
      airDate = str(datetime.now()),
      lastEditDate = str(datetime.now()),
    ))
    db.session.commit()

    return make_response(jsonify({'ret_url': url_for('adminpanel_content_season_edit', title_url=content.query.filter(and_(content.idContent == content_id, content.type == 'TV')).first().titleUrl, season_number=def_random_season_number)}))
###########################
###### end content->seasons
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

###########################
###### content->season->episodes
###########################
@app.route('/adminproc/content/season/episodes', methods=['POST'])
def adminproc_content_season_episodes():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    episode_id = request.get_json()['idTvEpisode']
    if not episode_id: return make_response(jsonify({'err_msg': '`episode_id` boş bırakıldı.'}))

    get_episode = tvEpisodeContent.query.filter(tvEpisodeContent.idTvEpisode == episode_id).first()
    if not get_episode: return make_response(jsonify({'err_msg': '`tvEpisodeContent->query` boş bırakıldı.'}))

    get_episode.drop()

    return make_response(jsonify({'succ_msg': 'Bölüm başarıyla silindi!'}))

  # TMDB IMPORT
  if get_function == 'tmdbImport':
    tmdb_id = request.get_json()['idTmdb'] 
    season_number = request.get_json()['seasonNumber']
    episode_number = request.get_json()['episodeNumber']

    check_content = content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'TV')).first()
    if not check_content: return make_response(jsonify({'err_msg': '`content->query` boş bırakıldı.'}))

    check_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == check_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
    if not check_season: return make_response(jsonify({'err_msg': '`tvSeasonContent->query` boş bırakıldı.'}))

    try:
      TMDBSimpleasy.TV.addEpisode(get_tmdb_id=tmdb_id, get_season_number=season_number, get_episode_number=episode_number)
      TMDBSimpleasy.TV.addPlayer(get_tmdb_id=tmdb_id, get_season_number=season_number, get_episode_number=episode_number)

      return make_response(jsonify({'ret_url', url_for('adminpanel_content_season_episodes', title_url=check_content.titleUrl, season_number=check_season.seasonNumber)}))
    except Exception as e: return make_response(jsonify({'err_msg': '{}'.format(e)}))

  # CREATE NATURAL
  if get_function == 'createNatural':
    content_id = request.get_json()['idContent']
    tv_season_id = request.get_json()['idTvSeason']
    if not content_id or not tv_season_id: pass

    def_random_id = id_generator(chars=string.digits, size=5)
    def_random_episode_number = randint(125125, 912859125)

    db.session.add(tvEpisodeContent(
      idTvSeason = tv_season_id,
      idContent = content_id,
      idAddProfile = get_logged_profile().idProfile,
      idAddAccount = get_logged_account().idAccount,
      title = 'İçerik {}'.format(def_random_id),
      overview = '#',
      idTmdb = '#',
      idImdb = '#',
      imagePoster = '/static/img/defaults/poster_episode.png',
      seasonNumber = tvSeasonContent.query.filter(tvSeasonContent.idTvSeason == tv_season_id).first().seasonNumber,
      episodeNumber = def_random_episode_number,
      visibility = 1,
      voteAverage = 0,
      airDate = str(datetime.now()),
      lastEditDate = str(datetime.now()),
    ))

    db.session.commit()

    return make_response(jsonify({'ret_url': url_for('adminpanel_content_season_episode_edit', title_url= content.query.filter(and_(content.idContent == content_id, content.type == 'TV')).first().titleUrl, season_number=tvSeasonContent.query.filter(tvSeasonContent.idTvSeason == tv_season_id).first().seasonNumber, episode_number=def_random_episode_number)}))
###########################
###### end content->season->episodes
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

############################
###### end content->season->episode->players
###########################
@app.route('/adminproc/content/season/episode/players', methods=['POST'])
def adminproc_content_season_episode_players():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    player_id = request.get_json()['idPlayer']
    if not player_id: return make_response(jsonify({'err_msg': '`player_id` boş bırakıldı.'}))

    get_player = tvPlayer.query.filter(tvPlayer.idPlayer == player_id).first()
    if not get_player: return make_response(jsonify({'err_msg': '`tvPlayer->query` boş bırakıldı.'}))

    get_player.drop()

    return make_response(jsonify({'succ_msg': 'Oynatıcı başarıyla silindi!'}))

  # TMDB IMPORT
  if get_function == 'tmdbImport':
    tmdb_id = request.get_json()['idTmdb'] 
    season_number = request.get_json()['seasonNumber']
    episode_number = request.get_json()['episodeNumber']

    check_content = content.query.filter(and_(content.idTmdb == str(tmdb_id), content.type == 'TV')).first()
    if not check_content: return make_response(jsonify({'err_msg': '`content->query` boş bırakıldı.'}))

    check_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == check_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
    if not check_season: return make_response(jsonify({'err_msg': '`tvSeasonContent->query` boş bırakıldı.'}))

    check_episode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == check_content.idContent, tvEpisodeContent.idTvSeason == check_season.idTvSeason, tvEpisodeContent.episodeNumber == episode_number)).first()
    if not check_episode: return make_response(jsonify({'err_msg': '`tvEpisodeContent->query` boş bırakıldı.'}))

    try:
      TMDBSimpleasy.TV.addPlayer(get_tmdb_id=tmdb_id, get_season_number=season_number, get_episode_number=episode_number)

      return make_response(jsonify({'ret_url', url_for('adminpanel_content_season_episode_players', title_url=check_content.titleUrl, season_number=check_season.seasonNumber, episode_number=check_episode.episodeNumber)}))
    except Exception as e: return make_response(jsonify({'err_msg': '{}'.format(e)}))

  # CREATE NATURAL
  if get_function == 'createNatural':
    content_id = request.get_json()['idContent']
    tv_season_id = request.get_json()['idTvSeason']
    tv_episode_id = request.get_json()['idTvEpisode']
    if not content_id or not tv_season_id or not tv_episode_id: pass

    def_random_id = id_generator(chars=string.digits, size=5)

    db.session.add(tvPlayer(
        idTvSeason = tv_season_id,
        idTvEpisode = tv_episode_id,
        idContent = content_id,
        idAddProfile = get_logged_profile().idProfile,
        idAddAccount = get_logged_account().idAccount,
        language = 'ORIGINAL',
        source = '#',
        title = 'İçerik {}'.format(def_random_id),
        type = 'PLYR',
        seasonNumber = tvSeasonContent.query.filter(tvSeasonContent.idTvSeason == tv_season_id).first().seasonNumber,
        episodeNumber = tvEpisodeContent.query.filter(tvEpisodeContent.idTvEpisode == tv_episode_id).first().episodeNumber,
        visibility = 1,
        order = 1,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
      ))

    db.session.commit()

    return make_response(jsonify({'ret_url': url_for('adminpanel_content_season_episode_player_edit', title_url=content.query.filter(and_(content.idContent == content_id, content.type == 'TV')).first().titleUrl, season_number=tvSeasonContent.query.filter(tvSeasonContent.idTvSeason == tv_season_id).first().seasonNumber, episode_number=tvEpisodeContent.query.filter(tvEpisodeContent.idTvEpisode == tv_episode_id).first().episodeNumber, view_key=tvPlayer.query.filter(tvPlayer.title == 'İçerik {}'.format(def_random_id)).first().viewKey)}))
##########################
###### end content->season->episode->players
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

##########################
###### accounts 
###########################
@app.route('/adminproc/accounts', methods=['POST'])
def adminproc_accounts():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    account_id = request.get_json()['idAccount']
    if not account_id: return make_response(jsonify({'err_msg': '`account_id` boş bırakıldı.'}))

    get_account = account.query.filter(account.idAccount == account_id).first()
    if not get_account: return make_response(jsonify({'err_msg': '`account->query` boş bırakıldı.'}))

    get_account.drop()

    return make_response(jsonify({'succ_msg': 'Hesap başarıyla silindi!'}))
##########################
###### end accounts 
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

##########################
###### profiles 
###########################
@app.route('/adminproc/profiles', methods=['POST'])
def adminproc_profiles():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    profile_id = request.get_json()['idProfile']
    if not profile_id: return make_response(jsonify({'err_msg': '`profile_id` boş bırakıldı.'}))

    get_profile = profile.query.filter(profile.idProfile == profile_id).first()
    if not get_profile: return make_response(jsonify({'err_msg': '`profile->query` boş bırakıldı.'}))

    get_profile.drop()

    return make_response(jsonify({'succ_msg': 'Profil başarıyla silindi!'}))
##########################
###### end profiles 
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

##########################
###### casts 
###########################
@app.route('/adminproc/casts', methods=['POST'])
def adminproc_casts():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    cast_id = request.get_json()['idCast']
    if not cast_id: return make_response(jsonify({'err_msg': '`cast_id` boş bırakıldı.'}))

    get_cast = cast.query.filter(cast.idCast == cast_id).first()
    if not get_cast: return make_response(jsonify({'err_msg': '`cast->query` boş bırakıldı.'}))

    get_cast.drop()

    return make_response(jsonify({'succ_msg': 'Hesap başarıyla silindi!'}))
##########################
###### end casts 
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

##########################
###### collections 
###########################
@app.route('/adminproc/collections', methods=['POST'])
def adminproc_collections():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    collection_id = request.get_json()['idCollection']
    if not collection_id: return make_response(jsonify({'err_msg': '`collection_id` boş bırakıldı.'}))

    get_collection = collection.query.filter(collection.idCollection == collection_id).first()
    if not get_collection: return make_response(jsonify({'err_msg': '`collection->query` boş bırakıldı.'}))

    get_collection.drop()

    return make_response(jsonify({'succ_msg': 'Hesap başarıyla silindi!'}))
##########################
###### end collections 
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

##########################
###### comments 
###########################
@app.route('/adminproc/comments', methods=['POST'])
def adminproc_comments():
  if not check_admin(): return make_response(jsonify({'err_msg': 'Yetkili değilsiniz.'}))

  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # DROP
  if get_function == 'drop':
    comment_id = request.get_json()['idComment']
    comment_type = request.get_json()['type']
    if not comment_id or not comment_type: return make_response(jsonify({'err_msg': '`comment_id` boş bırakıldı.'}))

    if comment_type == 'movie':
      get_comment = movieComment.query.filter(movieComment.idComment == comment_id).first()

    if comment_type == 'tv':
      get_comment = tvComment.query.filter(tvComment.idComment == comment_id).first()

    if comment_type == 'tv_title':
      get_comment = tvTitleComment.query.filter(tvTitleComment.idComment == comment_id).first()

    if comment_type == 'cast':
      get_comment = castComment.query.filter(castComment.idComment == comment_id).first()

    try:
      if not get_comment: return make_response(jsonify({'err_msg': '`comment->query` boş bırakıldı.'}))
      get_comment.drop()
      return make_response(jsonify({'succ_msg': 'Yorum başarıyla silindi!'}))
    except:
      return make_response(jsonify({'err_msg': 'HATA!'}))
##########################
###### end comments 
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################