# -*- encoding: utf-8 -*-
from includes import *

@app.route('/search', methods=['POST', 'GET'])
@app.route('/ara', methods=['POST', 'GET'])
def search():
  if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

  RET_URL = url_for('search') + '?query=*&page=1&type=*&sort=a-to-z'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_TYPE = request.args.get('type', default='*', type=str)
  ARG_SORT = request.args.get('sort', default='a-to-z', type=str)
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

  if not ARG_TYPE == '*':
    if ARG_TYPE == 'movie': _db_query_type = content.type == 'MOVIE'
    elif ARG_TYPE == 'tv': _db_query_type = content.type == 'TV'
    else: _db_query_type = content.type.like('%%')
  else: _db_query_type = content.type.like('%%')

  if ARG_SORT == 'a-to-z': _db_query_sort = content.title.asc()
  elif ARG_SORT == 'z-to-a': _db_query_sort = content.title.desc()
  elif ARG_SORT == 'newest': _db_query_sort = content.releaseDate.desc()
  elif ARG_SORT == 'oldest': _db_query_sort = content.releaseDate.asc()
  elif ARG_SORT == 'vote': _db_query_sort = content.voteAverage.desc()
  else: _db_query_sort = content.title.asc()
  # get query filters end

  # query
  get_results = content.query.filter(or_(and_(_db_query_title, _db_query_type), and_(_db_query_title_original, _db_query_type))).order_by(_db_query_sort).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(content.query.filter(or_(and_(_db_query_title, _db_query_type), and_(_db_query_title_original, _db_query_type))).all()) / DEF_LIST_COUNT)

  return render_template('search/index.html', title='İçerik Ara', list_results_info=get_results, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'type': ARG_TYPE,
                                          'sort': ARG_SORT,
                                          'list_count': DEF_LIST_COUNT,
                                        })

# BETA!
# args: ?query=*&page=1&genre=*&country=*&language=*&sort=a-to-z
@app.route('/search/<content_type>')
def search_beta(content_type:str='all'):
    if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

    # validation begin
    CONTENT_TYPES = ['all', 'movie', 'tv']
    ARGS = ['query', 'page', 'genre', 'country', 'language', 'sort']
    RET_URL = url_for('search_beta', content_type='all') + '?query=*&page=1&genre=*&country=*&language=*&sort=a-to-z'

    if not content_type in CONTENT_TYPES: return redirect(RET_URL)

    for _ in ARGS:
        if not request.args.get(_): return redirect(RET_URL)

    ARG_QUERY = request.args.get('query', default='*', type=str)
    ARG_PAGE = request.args.get('page', default=1, type=int)
    ARG_GENRE = request.args.get('genre', default='*', type=str)
    ARG_COUNTRY = request.args.get('country', default='*', type=str)
    ARG_LANGUAGE = request.args.get('language', default='*', type=str)
    ARG_SORT = request.args.get('sort', default='a-to-z', type=str)
    DEF_LIST_COUNT = 12
    DEF_OFFSET = (ARG_PAGE - 1) * DEF_LIST_COUNT
    # validation end 

    # filter begin
    if not ARG_QUERY == '*':
        _db_query_title = content.title.like('%{}%'.format(ARG_QUERY))
        _db_query_titleOriginal = content.titleOriginal.like('%{}%'.format(ARG_QUERY))
        _db_query_idTmdb = content.idTmdb.like('%{}%'.format(ARG_QUERY))
        _db_query_idImdb = content.idImdb.like('%{}%'.format(ARG_QUERY))
    else:
        _db_query_title = content.title.like('%%')
        _db_query_titleOriginal = content.titleOriginal.like('%%')
        _db_query_idTmdb = content.idTmdb.like('%%')
        _db_query_idImdb = content.idImdb.like('%%')

    if not content_type == 'all':
        if content_type == 'movie':
            _db_query_type = content.type == 'MOVIE'
        elif content_type == 'tv':
            _db_query_type = content.type == 'TV'
        else: _db_query_type = content.type.like('%%')
    else: _db_query_type = content.type.like('%%')

    if ARG_SORT == 'a-to-z': _db_query_sort = content.title.asc()
    elif ARG_SORT == 'z-to-a': _db_query_sort = content.title.desc()
    elif ARG_SORT == 'newest': _db_query_sort = content.releaseDate.desc()
    elif ARG_SORT == 'oldest': _db_query_sort = content.releaseDate.asc()
    elif ARG_SORT == 'vote': _db_query_sort = content.voteAverage.desc()
    else: _db_query_sort = content.title.asc()
    # filter end 

    # query begin
    #get_results = content.query.filter(or_(and_(_db_query_title, _db_query_type), and_(_db_query_titleOriginal, _db_query_type))).order_by(_db_query_sort).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
    #DEF_PAGE_MAX = ceil(len(content.query.filter(or_(and_(_db_query_title, _db_query_type), and_(_db_query_titleOriginal, _db_query_type))).all()) / DEF_LIST_COUNT)
    get_results = content.query.with_entities(content.idContent).join(contentLanguage, contentLanguage.idContent == content.idContent).filter().all()
    DEF_PAGE_MAX = 100
    # query end

    context = {
        'results': get_results,
    }

    return render_template('search/beta.html', title='İçerik Aranıyor', context=context, \
                                        _ARG = {
                                          'type': content_type,
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'genre': ARG_GENRE,
                                          'country': ARG_COUNTRY,
                                          'language': ARG_LANGUAGE,
                                          'sort': ARG_SORT,
                                          'list_count': DEF_LIST_COUNT,
                                        })
