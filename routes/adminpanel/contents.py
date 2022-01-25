# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/contents')
@app.route('/yoneticipaneli/icerikler')
def adminpanel_contents():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_contents') + '?query=*&page=1&type=*&sort=newest&list_count=10'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_TYPE = request.args.get('type', default='*', type=str)
  ARG_SORT = request.args.get('sort', default='newest', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if not ARG_QUERY == '*':
    _db_query_id = content.idContent.like('%{}%'.format(ARG_QUERY))
    _db_query_title = content.title.like('%{}%'.format(ARG_QUERY))
    _db_query_title_original = content.titleOriginal.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_id = content.idContent.like('%%')
    _db_query_title = content.title.like('%%')
    _db_query_title_original = content.title.like('%%')

  if not ARG_TYPE == '*': _db_type = content.type == ARG_TYPE
  else: _db_type = content.type.like('%%')

  if ARG_SORT == 'a-to-z': _db_sort = content.title.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = content.title.desc() 
  if ARG_SORT == 'newest': _db_sort = content.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = content.addDate.asc()

  get_results = content.query.filter(or_(and_(_db_query_id, _db_type), and_(_db_query_title, _db_type), and_(_db_query_title_original, _db_type))).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(content.query.filter(or_(and_(_db_query_id, _db_type), and_(_db_query_title, _db_type), and_(_db_query_title_original, _db_type))).all()) / ARG_LIST_COUNT)
  # get query filters end

  # url args validation begin
  if not request.args.get('query') or not request.args.get('page') or not request.args.get('type') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/contents/list.html', title='Tüm İçerikler', list_results_info=get_results, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'type': ARG_TYPE,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/content/<title_url>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/icerik/<title_url>/duzenle', methods=['POST', 'GET'])
def adminpanel_content_edit(title_url):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_content = content.query.filter(content.titleUrl == title_url).first()
  if not get_content: return redirect(RET_URL)

  try:
    get_posters_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'poster'))
    get_backgrounds_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'background'))
  except:
    get_posters_list = ''
    get_backgrounds_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_TITLE = request.form['input___title']
    DEF_NEW_TITLE_ORIGINAL = request.form['input___titleOriginal']
    DEF_NEW_TITLE_URL = request.form['input___titleUrl']
    DEF_NEW_OVERVIEW = request.form['input___overview']
    DEF_NEW_VOTE_AVERAGE = request.form['input___voteAverage']
    DEF_NEW_ID_TMDB = request.form['input___idTmdb']
    DEF_NEW_ID_IMDB = request.form['input___idImdb']
    # IMAGE UPLOAD BEGIN
    if request.form.getlist('poster'):
      DEF_NEW_IMAGE_POSTER = '/storage/content/{}/poster/{}'.format(get_content.idContent, request.form.getlist('poster')[0])
    else:
      temp_new_uploaded_poster = request.files['form__img-upload']
      if temp_new_uploaded_poster:
        temp_secure_filename = secure_filename(temp_new_uploaded_poster.filename)
        temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
        temp_new_uploaded_poster.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'poster', temp_generate_filename))
        DEF_NEW_IMAGE_POSTER = '/storage/content/{}/poster/{}'.format(get_content.idContent, temp_generate_filename)
      else:
        DEF_NEW_IMAGE_POSTER = request.form['input___imagePoster']

    if request.form.getlist('background'):
      DEF_NEW_IMAGE_BACKGROUND = '/storage/content/{}/background/{}'.format(get_content.idContent, request.form.getlist('background')[0])
    else:
      temp_new_uploaded_background = request.files['form__imgBg-upload']
      if temp_new_uploaded_background:
        temp_secure_filename = secure_filename(temp_new_uploaded_background.filename)
        temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
        temp_new_uploaded_background.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'background', temp_generate_filename))
        DEF_NEW_IMAGE_BACKGROUND = '/storage/content/{}/background/{}'.format(get_content.idContent, temp_generate_filename)
      else:
        DEF_NEW_IMAGE_BACKGROUND = request.form['input___imageBackground']
    # IMAGE UPLOAD END 
    DEF_NEW_RELEASE_DATE = request.form['input___releaseDate']
    DEF_NEW_ADULT = int(request.form['select2___adult'])
    DEF_NEW_VISIBILITY = int(request.form['select2___visibility'])
    DEF_NEW_TYPE = request.form['select2___type']

    # variable validation begin
    if not DEF_NEW_TITLE_URL: return error(err_msg='URL başlığını boş bıraktınız.', ret_url=RET_URL)
    # variable validation end

    check_content = content.query.filter(and_(content.idContent != get_content.idContent, content.titleUrl == DEF_NEW_TITLE_URL)).first()
    if check_content: return error(err_msg='Bu URL başlığı zaten kullanımda.', ret_url=RET_URL)

    get_content.title = DEF_NEW_TITLE
    get_content.titleOriginal = DEF_NEW_TITLE_ORIGINAL
    get_content.titleUrl = DEF_NEW_TITLE_URL
    get_content.overview = DEF_NEW_OVERVIEW
    get_content.voteAverage = DEF_NEW_VOTE_AVERAGE
    get_content.idTmdb = DEF_NEW_ID_TMDB
    get_content.idImdb = DEF_NEW_ID_IMDB
    get_content.imagePoster = DEF_NEW_IMAGE_POSTER
    get_content.imageBackground = DEF_NEW_IMAGE_BACKGROUND
    get_content.releaseDate = DEF_NEW_RELEASE_DATE
    get_content.adult = DEF_NEW_ADULT
    get_content.visibility = DEF_NEW_VISIBILITY
    get_content.type = DEF_NEW_TYPE

    db.session.commit()

    return redirect(url_for('adminpanel_content_edit', title_url=DEF_NEW_TITLE_URL))
  # form end 

  return render_template('adminpanel/contents/edit.html', sidebar=False, title='Düzenleniyor: {}'.format(get_content.title), content_info=get_content, posters_list_info=get_posters_list, backgrounds_list_info=get_backgrounds_list)

# **********************
# *
# * player section for movie contents begin
# *
# **********************

@app.route('/adminpanel/content/<title_url>/players')
@app.route('/yoneticipaneli/icerik/<title_url>/oynaticilar')
def adminpanel_content_players(title_url):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_content_players', title_url=title_url) + '?page=1&sort=order-asc&list_count=10'

  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_SORT = request.args.get('sort', default='order-asc', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if ARG_SORT == 'newest': _db_sort = moviePlayer.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = moviePlayer.addDate.asc()
  if ARG_SORT == 'order-asc': _db_sort = moviePlayer.order.asc()
  if ARG_SORT == 'order-desc': _db_sort = moviePlayer.order.desc()

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'MOVIE')).first()
  if not get_content: return redirect(url_for('adminpanel_home'))

  get_players = moviePlayer.query.filter(moviePlayer.idContent == get_content.idContent).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(moviePlayer.query.filter(moviePlayer.idContent == get_content.idContent).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()) / ARG_LIST_COUNT)
  # get query filters end

  # url args validation begin
  if not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/contents/players/list.html', sidebar=False, title='{} Tüm Oynatıcılar'.format(get_content.title), content_info=get_content, players_info=get_players, \
                                        _ARG = {
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/content/<title_url>/player/<view_key>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/icerik/<title_url>/oynatici/<view_key>/duzenle', methods=['POST', 'GET'])
def adminpanel_content_player_edit(title_url, view_key):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'MOVIE')).first()
  if not get_content: return redirect(RET_URL)

  get_player = moviePlayer.query.filter(and_(moviePlayer.idContent == get_content.idContent, moviePlayer.viewKey == view_key)).first()
  if not get_player: return redirect(RET_URL)

  try:
    get_players_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'player'))
  except:
    get_players_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_TITLE = request.form['input___title']
    DEF_NEW_VIEWKEY = get_player.viewKey # request.form['input___viewKey'] # ! we are not changing the view key
    # PLAYER UPLOAD BEGIN
    if request.form.getlist('player'):
      DEF_NEW_SOURCE = '/storage/content/{}/player/{}'.format(get_content.idContent, request.form.getlist('player')[0])
    else:
      temp_new_uploaded_player = request.files['form__img-upload']
      if temp_new_uploaded_player:
        temp_secure_filename = secure_filename(temp_new_uploaded_player.filename)
        temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
        temp_new_uploaded_player.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'player', temp_generate_filename))
        DEF_NEW_SOURCE = '/storage/content/{}/player/{}'.format(get_content.idContent, temp_generate_filename)
      else:
        DEF_NEW_SOURCE = request.form['input___source']
    # PLAYER UPLOAD END 
    DEF_NEW_ORDER = request.form['input___order']
    DEF_NEW_VISIBILITY = int(request.form['select2___visibility'])
    DEF_NEW_TYPE = request.form['select2___type']
    DEF_NEW_LANGUAGE = request.form['select2___language']

    # variable validation begin
    if not DEF_NEW_ORDER: return error(err_msg='Sıralama sayısı boş bıraktınız.', ret_url=RET_URL)
    # variable validation end

    get_player.title = DEF_NEW_TITLE
    get_player.viewKey = DEF_NEW_VIEWKEY
    get_player.source = DEF_NEW_SOURCE
    get_player.order = DEF_NEW_ORDER
    get_player.visibility = DEF_NEW_VISIBILITY
    get_player.type = DEF_NEW_TYPE
    get_player.language = DEF_NEW_LANGUAGE

    db.session.commit()

    return redirect(url_for('adminpanel_content_player_edit', title_url=get_content.titleUrl, view_key=DEF_NEW_VIEWKEY))
  # form end 

  return render_template('adminpanel/contents/players/edit.html', sidebar=False, title='Düzenleniyor: {} {} Oynatıcısı'.format(get_content.title, get_player.title), content_info=get_content, player_info=get_player, players_list_info=get_players_list)

# **********************
# *
# * player section for movie contents end 
# *
# **********************

@app.route('/adminpanel/content/<title_url>/seasons')
@app.route('/yoneticipaneli/icerik/<title_url>/sezonlar')
def adminpanel_content_seasons(title_url):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_content_seasons', title_url=title_url) + '?page=1&sort=season-asc&list_count=10'

  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_SORT = request.args.get('sort', default='season-asc', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if ARG_SORT == 'a-to-z': _db_sort = tvSeasonContent.title.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = tvSeasonContent.title.desc() 
  if ARG_SORT == 'newest': _db_sort = tvSeasonContent.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = tvSeasonContent.addDate.asc()
  if ARG_SORT == 'season-asc': _db_sort = tvSeasonContent.seasonNumber.asc()
  if ARG_SORT == 'season-desc': _db_sort = tvSeasonContent.seasonNumber.desc()

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if not get_content: return redirect(url_for('adminpanel_home'))

  get_seasons = tvSeasonContent.query.filter(tvSeasonContent.idContent == get_content.idContent).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(tvSeasonContent.query.filter(tvSeasonContent.idContent == get_content.idContent).all()) / ARG_LIST_COUNT)
  # get query filters end

  # url args validation begin
  if not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/contents/seasons/list.html', sidebar=False, title='{} Tüm Sezonlar'.format(get_content.title), content_info=get_content, seasons_info=get_seasons, \
                                        _ARG = {
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/content/<title_url>/season/<season_number>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/icerik/<title_url>/sezon/<season_number>/duzenle', methods=['POST', 'GET'])
def adminpanel_content_season_edit(title_url, season_number):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if not get_content: return redirect(RET_URL)

  get_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == get_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
  if not get_season: return redirect(RET_URL)

  try:
    get_posters_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'season', get_season.idTvSeason, 'poster'))
  except:
    get_posters_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_TITLE = request.form['input___title']
    DEF_NEW_OVERVIEW = request.form['input___overview']
    DEF_NEW_ID_TMDB = request.form['input___idTmdb']
    # IMAGE UPLOAD BEGIN
    if request.form.getlist('poster'):
      DEF_NEW_IMAGE_POSTER = '/storage/content/{}/season/{}/poster/{}'.format(get_content.idContent, get_season.idTvSeason, request.form.getlist('poster')[0])
    else:
      temp_new_uploaded_poster = request.files['form__img-upload']
      if temp_new_uploaded_poster:
        temp_secure_filename = secure_filename(temp_new_uploaded_poster.filename)
        temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
        temp_new_uploaded_poster.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'season', get_season.idTvSeason, 'poster', temp_generate_filename))
        DEF_NEW_IMAGE_POSTER = '/storage/content/{}/season/{}/poster/{}'.format(get_content.idContent, get_season.idTvSeason, temp_generate_filename)
      else:
        DEF_NEW_IMAGE_POSTER = request.form['input___imagePoster']
    # IMAGE UPLOAD END 

    DEF_NEW_SEASON_NUMBER = request.form['input___seasonNumber']
    DEF_NEW_AIR_DATE = request.form['input___airDate']
    DEF_NEW_VISIBILITY = int(request.form['select2___visibility'])

    # variable validation begin
    if not DEF_NEW_SEASON_NUMBER: return error(err_msg='Sezon numarasını boş bıraktınız.', ret_url=RET_URL)
    else:
      # check if there is a season with DEF_NEW_SEASON_NUMBER in this content
      if tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == get_content.idContent, tvSeasonContent.idTvSeason != get_season.idTvSeason, tvSeasonContent.seasonNumber == DEF_NEW_SEASON_NUMBER)).first():
        return error(err_msg='Bu içerik için bu sezon zaten halihazırda mevcut.', ret_url=RET_URL)
    # variable validation end

    get_season.title = DEF_NEW_TITLE
    get_season.overview = DEF_NEW_OVERVIEW
    get_season.idTmdb = DEF_NEW_ID_TMDB
    get_season.imagePoster = DEF_NEW_IMAGE_POSTER
    get_season.seasonNumber = DEF_NEW_SEASON_NUMBER
    get_season.airDate = DEF_NEW_AIR_DATE
    get_season.visibility = DEF_NEW_VISIBILITY

    db.session.commit()

    return redirect(url_for('adminpanel_content_season_edit', title_url=get_content.titleUrl, season_number=DEF_NEW_SEASON_NUMBER))
  # form end 

  return render_template('adminpanel/contents/seasons/edit.html', sidebar=False, title='Düzenleniyor: {} {}. Sezon'.format(get_content.title, get_season.seasonNumber), content_info=get_content, season_info=get_season, posters_list_info=get_posters_list)

@app.route('/adminpanel/content/<title_url>/season/<season_number>/episodes')
@app.route('/yoneticipaneli/icerik/<title_url>/sezon/<season_number>/bolumler')
def adminpanel_content_season_episodes(title_url, season_number):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_content_season_episodes', title_url=title_url, season_number=season_number) + '?page=1&sort=episode-asc&list_count=10'

  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_SORT = request.args.get('sort', default='episode-asc', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if ARG_SORT == 'a-to-z': _db_sort = tvEpisodeContent.title.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = tvEpisodeContent.title.desc() 
  if ARG_SORT == 'newest': _db_sort = tvEpisodeContent.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = tvEpisodeContent.addDate.asc()
  if ARG_SORT == 'episode-asc': _db_sort = tvEpisodeContent.episodeNumber.asc()
  if ARG_SORT == 'episode-desc': _db_sort = tvEpisodeContent.episodeNumber.desc()

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if not get_content: return redirect(url_for('adminpanel_home'))

  get_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == get_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
  if not get_season: return redirect(url_for('adminpanel_home'))

  get_episodes = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == get_content.idContent, tvEpisodeContent.idTvSeason == get_season.idTvSeason)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == get_content.idContent, tvEpisodeContent.idTvSeason == get_season.idTvSeason)).all()) / ARG_LIST_COUNT)
  # get query filters end

  # url args validation begin
  if not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/contents/seasons/episodes/list.html', sidebar=False, title='{} {}. Sezon Tüm Bölümler'.format(get_content.title, get_season.seasonNumber), content_info=get_content, season_info=get_season, episodes_info=get_episodes, \
                                        _ARG = {
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/content/<title_url>/season/<season_number>/episode/<episode_number>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/icerik/<title_url>/sezon/<season_number>/bolum/<episode_number>/duzenle', methods=['POST', 'GET'])
def adminpanel_content_season_episode_edit(title_url, season_number, episode_number):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if not get_content: return redirect(RET_URL)

  get_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == get_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
  if not get_season: return redirect(RET_URL)

  get_episode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == get_content.idContent, tvEpisodeContent.seasonNumber == season_number, tvEpisodeContent.episodeNumber == episode_number)).first()
  if not get_episode: return redirect(RET_URL)

  try:
    get_posters_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'season', get_season.idTvSeason, 'episode', get_episode.idTvEpisode, 'poster'))
  except:
    get_posters_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_TITLE = request.form['input___title']
    DEF_NEW_OVERVIEW = request.form['input___overview']
    DEF_NEW_VOTE_AVERAGE = request.form['input___voteAverage']
    DEF_NEW_ID_TMDB = request.form['input___idTmdb']
    DEF_NEW_ID_IMDB = request.form['input___idImdb']
    # IMAGE UPLOAD BEGIN
    if request.form.getlist('poster'):
      DEF_NEW_IMAGE_POSTER = '/storage/content/{}/season/{}/episode/{}/poster/{}'.format(get_content.idContent, get_season.idTvSeason, get_episode.idTvEpisode, request.form.getlist('poster')[0])
    else:
      temp_new_uploaded_poster = request.files['form__img-upload']
      if temp_new_uploaded_poster:
        temp_secure_filename = secure_filename(temp_new_uploaded_poster.filename)
        temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
        temp_new_uploaded_poster.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'season', get_season.idTvSeason, 'episode', get_episode.idTvEpisode, 'poster', temp_generate_filename))
        DEF_NEW_IMAGE_POSTER = '/storage/content/{}/season/{}/episode/{}/poster/{}'.format(get_content.idContent, get_season.idTvSeason, get_episode.idTvEpisode, temp_generate_filename)
      else:
        DEF_NEW_IMAGE_POSTER = request.form['input___imagePoster']
    # IMAGE UPLOAD END 
    DEF_NEW_SEASON_NUMBER = get_episode.seasonNumber # request.form['input___seasonNumber'] # ! we are not changing the season number
    DEF_NEW_EPISODE_NUMBER = request.form['input___episodeNumber']
    DEF_NEW_AIR_DATE = request.form['input___airDate']
    DEF_NEW_VISIBILITY = int(request.form['select2___visibility'])

    # variable validation begin
    if not DEF_NEW_EPISODE_NUMBER: return error(err_msg='Bölüm sayısı boş bıraktınız.', ret_url=RET_URL)
    # variable validation end

    get_episode.title = DEF_NEW_TITLE
    get_episode.overview = DEF_NEW_OVERVIEW
    get_episode.voteAverage = DEF_NEW_VOTE_AVERAGE
    get_episode.idTmdb = DEF_NEW_ID_TMDB
    get_episode.idImdb = DEF_NEW_ID_IMDB
    get_episode.imagePoster = DEF_NEW_IMAGE_POSTER
    get_episode.seasonNumber = DEF_NEW_SEASON_NUMBER # ! we are not changing the season number
    get_episode.episodeNumber = DEF_NEW_EPISODE_NUMBER
    get_episode.airDate = DEF_NEW_AIR_DATE
    get_episode.visibility = DEF_NEW_VISIBILITY

    db.session.commit()

    return redirect(url_for('adminpanel_content_season_episode_edit', title_url=get_content.titleUrl, season_number=DEF_NEW_SEASON_NUMBER, episode_number=DEF_NEW_EPISODE_NUMBER))
  # form end 

  return render_template('adminpanel/contents/seasons/episodes/edit.html', sidebar=False, title='Düzenleniyor: {} {}. Sezon {}. Bölüm'.format(get_content.title, get_season.seasonNumber, get_episode.episodeNumber), content_info=get_content, season_info=get_season, episode_info=get_episode, posters_list_info=get_posters_list)

@app.route('/adminpanel/content/<title_url>/season/<season_number>/episode/<episode_number>/players')
@app.route('/yoneticipaneli/icerik/<title_url>/sezon/<season_number>/bolum/<episode_number>/oynaticilar')
def adminpanel_content_season_episode_players(title_url, season_number, episode_number):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_content_season_episode_players', title_url=title_url, season_number=season_number, episode_number=episode_number) + '?page=1&sort=order-asc&list_count=10'

  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_SORT = request.args.get('sort', default='order-asc', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if ARG_SORT == 'newest': _db_sort = tvPlayer.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = tvPlayer.addDate.asc()
  if ARG_SORT == 'order-asc': _db_sort = tvPlayer.order.asc()
  if ARG_SORT == 'order-desc': _db_sort = tvPlayer.order.desc()

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if not get_content: return redirect(url_for('adminpanel_home'))

  get_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == get_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
  if not get_season: return redirect(url_for('adminpanel_home'))

  get_episode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == get_content.idContent, tvEpisodeContent.idTvSeason == get_season.idTvSeason, tvEpisodeContent.seasonNumber == season_number, tvEpisodeContent.episodeNumber == episode_number)).first()
  if not get_episode: return redirect(url_for('adminpanel_home'))

  get_players = tvPlayer.query.filter(and_(tvPlayer.idContent == get_content.idContent, tvPlayer.idTvSeason == get_season.idTvSeason, tvPlayer.idTvEpisode == get_episode.idTvEpisode, tvPlayer.seasonNumber == season_number, tvPlayer.episodeNumber == episode_number)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(tvPlayer.query.filter(and_(tvPlayer.idContent == get_content.idContent, tvPlayer.idTvSeason == get_season.idTvSeason, tvPlayer.idTvEpisode == get_episode.idTvEpisode, tvPlayer.seasonNumber == season_number, tvPlayer.episodeNumber == episode_number)).all()) / ARG_LIST_COUNT)
  # get query filters end

  # url args validation begin
  if not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/contents/seasons/episodes/players/list.html', sidebar=False, title='{} {}. Sezon {}. Bölüm Tüm Oynatıcılar'.format(get_content.title, get_season.seasonNumber, get_episode.episodeNumber), content_info=get_content, season_info=get_season, episode_info=get_episode, players_info=get_players, \
                                        _ARG = {
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/content/<title_url>/season/<season_number>/episode/<episode_number>/player/<view_key>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/icerik/<title_url>/sezon/<season_number>/bolum/<episode_number>/oynatici/<view_key>/duzenle', methods=['POST', 'GET'])
def adminpanel_content_season_episode_player_edit(title_url, season_number, episode_number, view_key):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if not get_content: return redirect(RET_URL)

  get_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == get_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
  if not get_season: return redirect(RET_URL)

  get_episode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == get_content.idContent, tvEpisodeContent.seasonNumber == season_number, tvEpisodeContent.episodeNumber == episode_number)).first()
  if not get_episode: return redirect(RET_URL)

  get_player = tvPlayer.query.filter(and_(tvPlayer.idContent == get_content.idContent, tvPlayer.idTvSeason == get_season.idTvSeason, tvPlayer.idTvEpisode == get_episode.idTvEpisode, tvPlayer.viewKey == view_key, tvPlayer.seasonNumber == season_number, tvPlayer.episodeNumber == episode_number)).first()
  if not get_player: return redirect(RET_URL)

  try:
    get_players_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'season', get_season.idTvSeason, 'episode', get_episode.idTvEpisode, 'player'))
  except:
    get_players_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_TITLE = request.form['input___title']
    DEF_NEW_VIEWKEY = get_player.viewKey # request.form['input___viewKey'] # ! we are not changing the view key
    # PLAYER UPLOAD BEGIN
    if request.form.getlist('player'):
      DEF_NEW_SOURCE = '/storage/content/{}/season/{}/episode/{}/player/{}'.format(get_content.idContent, get_season.idTvSeason, get_episode.idTvEpisode, request.form.getlist('player')[0])
    else:
      temp_new_uploaded_player = request.files['form__img-upload']
      if temp_new_uploaded_player:
        temp_secure_filename = secure_filename(temp_new_uploaded_player.filename)
        temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
        temp_new_uploaded_player.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'content', get_content.idContent, 'season', get_season.idTvSeason, 'episode', get_episode.idTvEpisode, 'player', temp_generate_filename))
        DEF_NEW_SOURCE = '/storage/content/{}/season/{}/episode/{}/player/{}'.format(get_content.idContent, get_season.idTvSeason, get_episode.idTvEpisode, temp_generate_filename)
      else:
        DEF_NEW_SOURCE = request.form['input___source']
    # PLAYER UPLOAD END 
    DEF_NEW_ORDER = request.form['input___order']
    DEF_NEW_SEASON_NUMBER = get_player.seasonNumber # request.form['input___seasonNumber'] # ! we are not changing the season number
    DEF_NEW_EPISODE_NUMBER = get_player.episodeNumber # request.form['input___episodeNumber'] # ! we are not changing the season number
    DEF_NEW_VISIBILITY = int(request.form['select2___visibility'])
    DEF_NEW_TYPE = request.form['select2___type']
    DEF_NEW_LANGUAGE = request.form['select2___language']

    # variable validation begin
    if not DEF_NEW_ORDER: return error(err_msg='Sıralama sayısı boş bıraktınız.', ret_url=RET_URL)
    # variable validation end

    get_player.title = DEF_NEW_TITLE
    get_player.viewKey = DEF_NEW_VIEWKEY
    get_player.source = DEF_NEW_SOURCE
    get_player.order = DEF_NEW_ORDER
    get_player.seasonNumber = DEF_NEW_SEASON_NUMBER # ! we are not changing the season number
    get_player.episodeNumber = DEF_NEW_EPISODE_NUMBER # ! we are not changing the episode number
    get_player.visibility = DEF_NEW_VISIBILITY
    get_player.type = DEF_NEW_TYPE
    get_player.language = DEF_NEW_LANGUAGE

    db.session.commit()

    return redirect(url_for('adminpanel_content_season_episode_player_edit', title_url=get_content.titleUrl, season_number=DEF_NEW_SEASON_NUMBER, episode_number=DEF_NEW_EPISODE_NUMBER, view_key=DEF_NEW_VIEWKEY))
  # form end 

  return render_template('adminpanel/contents/seasons/episodes/players/edit.html', sidebar=False, title='Düzenleniyor: {} {}. Sezon {}. Bölüm {} Oynatıcısı'.format(get_content.title, get_season.seasonNumber, get_episode.episodeNumber, get_player.title), content_info=get_content, season_info=get_season, episode_info=get_episode, player_info=get_player, players_list_info=get_players_list)
