# -*- encoding: utf-8 -*-
from includes import *

# beta! working on it.
# url parameters:
"""
?query
&page
&genre
&language
&country
&actor
"""
@app.route('/catalog/<content_type>', methods=['GET'])
def catalog_beta(content_type):
    if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

    RET_URL = url_for('catalog_beta', content_type=content_type) + '?query=*&page=1&genre=*&language=*&country=*&actor=*'

    CONTENT_TYPES = ['movie', 'tv']
    ARGS = ['query', 'page', 'genre', 'language', 'country', 'actor']
    ARG_CONTENT_TYPE = content_type.upper()
    ARG_QUERY = request.args.get('query', default='*', type=str)
    ARG_PAGE = request.args.get('page', default=1, type=int)
    ARG_GENRE = request.args.get('genre', default='*', type=str)
    ARG_LANGUAGE = request.args.get('language', default='*', type=str)
    ARG_COUNTRY = request.args.get('country', default='*', type=str)
    ARG_ACTOR = request.args.get('actor', default='*', type=str)
    DEF_LIST_COUNT = 12
    DEF_OFFSET = (ARG_PAGE - 1) * DEF_LIST_COUNT

    # page parameters validation begin
    if not content_type in CONTENT_TYPES: return redirect(url_for('home'))

    if not ARG_PAGE >= 1: return redirect(RET_URL)

    for __arg in ARGS:
        if not request.args.get(__arg): return redirect(RET_URL)
    # page parameters validation end

    # query begin
    if content_type == 'movie': querygenre = movieContentGenre
    elif content_type == 'tv': querygenre = tvContentGenre
    else: return redirect(url_for('home'))

    if ARG_QUERY == '*': queryparam_query = content.title.like('%%')
    else: queryparam_query = content.title.like('%{}%'.format(ARG_QUERY))

    if ARG_GENRE == '*': queryparam_genre = querygenre.idGenre.like('%%')
    else: queryparam_genre = querygenre.idGenre.like('%{}%'.format(ARG_GENRE))

    if ARG_LANGUAGE == '*': queryparam_language = contentLanguage.idISO_639_1.like('%%')
    else: queryparam_language = contentLanguage.idISO_639_1.like('%{}%'.format(ARG_LANGUAGE))

    if ARG_COUNTRY == '*': queryparam_country = contentCountry.idISO_3166_1.like('%%')
    else: queryparam_country = contentCountry.idISO_3166_1.like('%{}%'.format(ARG_COUNTRY))

    if ARG_ACTOR == '*': queryparam_actor = contentCast.idCast.like('%%')
    else: queryparam_actor = contentCast.idCast.like('%{}%'.format(ARG_ACTOR))

    queryset = content.query.distinct().join(querygenre).join(contentLanguage).join(contentCountry).join(contentCast).filter(content.type == ARG_CONTENT_TYPE, queryparam_query, queryparam_genre, queryparam_language, queryparam_country, queryparam_actor).order_by(content.title.asc()).paginate(ARG_PAGE, DEF_LIST_COUNT, error_out=False)

    return render_template('catalog/test.html', queryset=queryset)
    # query end

    return str(queryset)

@app.route('/movies', methods=['POST', 'GET'])
@app.route('/filmler', methods=['POST', 'GET'])
def catalog_movie():
  if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

  RET_URL = url_for('catalog_tv') + '?query=*&page=1&genre=*'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_GENRE = request.args.get('genre', default='*', type=str)
  DEF_LIST_COUNT = 12
  DEF_OFFSET = (ARG_PAGE - 1) * DEF_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL)
  # page validation end

  # get query filters begin
  if not ARG_QUERY == '*':
    _db_query_title = content.title.like('%{}%'.format(ARG_QUERY))
    _db_query_title_original = content.titleOriginal.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_title = content.title.like('%%')
    _db_query_title_original = content.titleOriginal.like('%%')

  # query without genre filtering
  get_results = content.query.filter(or_(and_(_db_query_title, content.type == 'MOVIE'), and_(_db_query_title_original, content.type == 'MOVIE'))).order_by(content.title.asc()).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(content.query.filter(or_(and_(_db_query_title, content.type == 'MOVIE'), and_(_db_query_title_original, content.type == 'MOVIE'))).all()) / DEF_LIST_COUNT)

  if not ARG_GENRE == '*':
    if tvGenreList.query.filter(tvGenreList.idGenre == ARG_GENRE).first():
      _def_genre = movieContentGenre.idGenre == ARG_GENRE

      # query with genre filtering
      get_results = content.query.join(movieContentGenre).filter(or_(and_(_db_query_title, content.type == 'MOVIE', movieContentGenre.idGenre == ARG_GENRE), and_(_db_query_title_original, content.type == 'MOVIE', movieContentGenre.idGenre == ARG_GENRE))).order_by(content.title.asc()).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
      DEF_PAGE_MAX = ceil(len(content.query.join(movieContentGenre).filter(or_(and_(_db_query_title, content.type == 'MOVIE', movieContentGenre.idGenre == ARG_GENRE), and_(_db_query_title_original, content.type == 'MOVIE', movieContentGenre.idGenre == ARG_GENRE))).all()) / DEF_LIST_COUNT)
  # get query filters end

  return render_template('catalog/index.html', title='Filmler', list_results_info=get_results, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'genre': ARG_GENRE,
                                          'list_count': DEF_LIST_COUNT,
                                        })

@app.route('/tv', methods=['POST', 'GET'])
@app.route('/diziler', methods=['POST', 'GET'])
def catalog_tv():
  if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

  RET_URL = url_for('catalog_tv') + '?query=*&page=1&genre=*'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_GENRE = request.args.get('genre', default='*', type=str)
  DEF_LIST_COUNT = 12
  DEF_OFFSET = (ARG_PAGE - 1) * DEF_LIST_COUNT

  # page parameter validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL)
  # page parameter validation end

  # get query filters begin
  if not ARG_QUERY == '*':
    _db_query_title = content.title.like('%{}%'.format(ARG_QUERY))
    _db_query_title_original = content.titleOriginal.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_title = content.title.like('%%')
    _db_query_title_original = content.titleOriginal.like('%%')

  # query without genre filtering
  get_results = content.query.filter(or_(and_(_db_query_title, content.type == 'TV'), and_(_db_query_title_original, content.type == 'TV'))).order_by(content.title.asc()).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(content.query.filter(or_(and_(_db_query_title, content.type == 'TV'), and_(_db_query_title_original, content.type == 'TV'))).all()) / DEF_LIST_COUNT)

  if not ARG_GENRE == '*':
    if tvGenreList.query.filter(tvGenreList.idGenre == ARG_GENRE).first():
      _def_genre = tvContentGenre.idGenre == ARG_GENRE

      # query with genre filtering
      get_results = content.query.join(tvContentGenre).filter(or_(and_(_db_query_title, content.type == 'TV', tvContentGenre.idGenre == ARG_GENRE), and_(_db_query_title_original, content.type == 'TV', tvContentGenre.idGenre == ARG_GENRE))).order_by(content.title.asc()).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
      DEF_PAGE_MAX = ceil(len(content.query.join(tvContentGenre).filter(or_(and_(_db_query_title, content.type == 'TV', tvContentGenre.idGenre == ARG_GENRE), and_(_db_query_title_original, content.type == 'TV', tvContentGenre.idGenre == ARG_GENRE))).all()) / DEF_LIST_COUNT)
  # get query filters end

  return render_template('catalog/index.html', title='Diziler', list_results_info=get_results, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'genre': ARG_GENRE,
                                          'list_count': DEF_LIST_COUNT,
                                        })
