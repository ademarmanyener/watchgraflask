# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/v2/list')
def adminpanel_v2_list():
    if not check_admin(): return redirect(url_for('home'))

    RET_URL = url_for('adminpanel_v2_home')

    ARG_TABLE = request.args.get('table', default=None, type=str)
    ARG_QUERY = request.args.get('query', default='*', type=str)
    ARG_PAGE = request.args.get('page', default=1, type=int)
    ARG_SORT = request.args.get('sort', default='newest', type=str)
    ARG_LIST_COUNT = request.args.get('list_count', default=25, type=int)
    DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

    # page validation begin
    if not ARG_PAGE >= 1: return redirect(RET_URL) 
    # page validation end

    if ARG_TABLE:
        # `content` table begin
        if ARG_TABLE == 'content':

            RET_URL = url_for('adminpanel_v2_list') + '?table=content&query=*&page=1&sort=newest&list_count=25'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = content.idContent.like('%{}%'.format(ARG_QUERY))
                _db_query_title = content.title.like('%{}%'.format(ARG_QUERY))
                _db_query_original_title = content.titleOriginal.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = content.idContent.like('%%')
                _db_query_title = content.title.like('%%')
                _db_query_original_title = content.titleOriginal.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = content.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = content.title.desc() 
            if ARG_SORT == 'newest': _db_sort = content.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = content.addDate.asc()
            # sort end

            # fetch begin
            get_results = content.query.filter(or_(_db_query_id, _db_query_title, _db_query_original_title)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(content.query.filter(or_(_db_query_id, _db_query_title, _db_query_original_title)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='İçerikler', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `content` table end 

        # `tvseasoncontent` table begin
        if ARG_TABLE == 'tvseasoncontent':

            RET_URL = url_for('adminpanel_v2_list') + '?table=tvseasoncontent&query=*&idContent=*&page=1&sort=season&list_count=25'

            ARG_CONTENT_ID = request.args.get('idContent', default='*', type=str)

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = tvSeasonContent.idTvSeason.like('%{}%'.format(ARG_QUERY))
                _db_query_title = tvSeasonContent.title.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = tvSeasonContent.idTvSeason.like('%%')
                _db_query_title = tvSeasonContent.title.like('%%')
            # query end 

            # content id begin
            if not ARG_CONTENT_ID == "*":
                if content.query.filter_by(idContent=ARG_CONTENT_ID).first():
                    if content.query.filter_by(idContent=ARG_CONTENT_ID).first().type == 'TV':
                        _db_query_content_id = tvSeasonContent.idContent == '{}'.format(ARG_CONTENT_ID)
                    else:
                        _db_query_content_id = tvSeasonContent.idContent.like('%%')
                else:
                    _db_query_content_id = tvSeasonContent.idContent.like('%%')
            else:
                _db_query_content_id = tvSeasonContent.idContent.like('%%')
            # content id begin

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = tvSeasonContent.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = tvSeasonContent.title.desc() 
            if ARG_SORT == 'newest': _db_sort = tvSeasonContent.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = tvSeasonContent.addDate.asc()
            if ARG_SORT == 'season': _db_sort = tvSeasonContent.seasonNumber.asc()
            # sort end

            # fetch begin
            get_results = tvSeasonContent.query.filter(and_(or_(_db_query_id, _db_query_title), _db_query_content_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(tvSeasonContent.query.filter(and_(or_(_db_query_id, _db_query_title), _db_query_content_id)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('idContent') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Sezonlar', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'idContent': ARG_CONTENT_ID,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }, \
                                                                    content=content, tvEpisodeContent=tvEpisodeContent, tmdb=tmdb) 
        # `tvseasoncontent` table end 

        # `tvepisodecontent` table begin
        if ARG_TABLE == 'tvepisodecontent':

            RET_URL = url_for('adminpanel_v2_list') + '?table=tvepisodecontent&query=*&idContent=*&idTvSeason=*&page=1&sort=episode&list_count=25'

            ARG_CONTENT_ID = request.args.get('idContent', default='*', type=str)
            ARG_TV_SEASON_ID = request.args.get('idTvSeason', default='*', type=str)

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = tvEpisodeContent.idTvEpisode.like('%{}%'.format(ARG_QUERY))
                _db_query_title = tvEpisodeContent.title.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = tvEpisodeContent.idTvEpisode.like('%%')
                _db_query_title = tvEpisodeContent.title.like('%%')
            # query end 

            # content id begin
            if not ARG_CONTENT_ID == "*":
                if content.query.filter_by(idContent=ARG_CONTENT_ID).first():
                    if content.query.filter_by(idContent=ARG_CONTENT_ID).first().type == 'TV':
                        _db_query_content_id = tvEpisodeContent.idContent == '{}'.format(ARG_CONTENT_ID)
                    else:
                        _db_query_content_id = tvEpisodeContent.idContent.like('%%')
                else:
                    _db_query_content_id = tvEpisodeContent.idContent.like('%%')
            else:
                _db_query_content_id = tvEpisodeContent.idContent.like('%%')
            # content id begin

            # tv season id begin
            if not ARG_TV_SEASON_ID == "*":
                if tvSeasonContent.query.filter_by(idTvSeason=ARG_TV_SEASON_ID).first():
                    _db_query_tv_season_id = tvEpisodeContent.idTvSeason == '{}'.format(ARG_TV_SEASON_ID)
                else:
                    _db_query_tv_season_id = tvEpisodeContent.idTvSeason.like('%%')
            else:
                _db_query_tv_season_id = tvEpisodeContent.idTvSeason.like('%%')
            # tv season id end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = tvEpisodeContent.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = tvEpisodeContent.title.desc() 
            if ARG_SORT == 'newest': _db_sort = tvEpisodeContent.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = tvEpisodeContent.addDate.asc()
            if ARG_SORT == 'episode': _db_sort = tvEpisodeContent.episodeNumber.asc()
            # sort end

            # fetch begin
            get_results = tvEpisodeContent.query.filter(and_(or_(_db_query_id, _db_query_title), _db_query_content_id, _db_query_tv_season_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(tvEpisodeContent.query.filter(and_(or_(_db_query_id, _db_query_title), _db_query_content_id, _db_query_tv_season_id)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('idContent') or not request.args.get('idTvSeason') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Bölümler', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'idContent': ARG_CONTENT_ID,
                                                                        'idTvSeason': ARG_TV_SEASON_ID,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }, \
                                                                    content=content, tvSeasonContent=tvSeasonContent, tmdb=tmdb) 
        # `tvepisodecontent` table end 

        # `tvplayer` table begin
        if ARG_TABLE == 'tvplayer':

            RET_URL = url_for('adminpanel_v2_list') + '?table=tvplayer&query=*&idContent=*&idTvSeason=*&idTvEpisode=*&page=1&sort=newest&list_count=25'

            ARG_CONTENT_ID = request.args.get('idContent', default='*', type=str)
            ARG_TV_SEASON_ID = request.args.get('idTvSeason', default='*', type=str)
            ARG_TV_EPISODE_ID = request.args.get('idTvEpisode', default='*', type=str)

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = tvPlayer.idPlayer.like('%{}%'.format(ARG_QUERY))
                _db_query_title = tvPlayer.title.like('%{}%'.format(ARG_QUERY))
                _db_query_viewKey = tvPlayer.viewKey.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = tvPlayer.idPlayer.like('%%')
                _db_query_title = tvPlayer.title.like('%%')
                _db_query_viewKey = tvPlayer.viewKey.like('%%')
            # query end 

            # content id begin
            if not ARG_CONTENT_ID == "*":
                if content.query.filter_by(idContent=ARG_CONTENT_ID).first():
                    if content.query.filter_by(idContent=ARG_CONTENT_ID).first().type == 'TV':
                        _db_query_content_id = tvPlayer.idContent == '{}'.format(ARG_CONTENT_ID)
                    else:
                        _db_query_content_id = tvPlayer.idContent.like('%%')
                else:
                    _db_query_content_id = tvPlayer.idContent.like('%%')
            else:
                _db_query_content_id = tvPlayer.idContent.like('%%')
            # content id begin

            # tv season id begin
            if not ARG_TV_SEASON_ID == "*":
                if tvSeasonContent.query.filter_by(idTvSeason=ARG_TV_SEASON_ID).first():
                    _db_query_tv_season_id = tvPlayer.idTvSeason == '{}'.format(ARG_TV_SEASON_ID)
                else:
                    _db_query_tv_season_id = tvPlayer.idTvSeason.like('%%')
            else:
                _db_query_tv_season_id = tvPlayer.idTvSeason.like('%%')
            # tv season id end 

            # tv episode id begin
            if not ARG_TV_EPISODE_ID == '*':
                if tvEpisodeContent.query.filter_by(idTvEpisode=ARG_TV_EPISODE_ID).first():
                    _db_query_tv_episode_id = tvPlayer.idTvEpisode == '{}'.format(ARG_TV_EPISODE_ID)
                else:
                    _db_query_tv_episode_id = tvPlayer.idTvEpisode.like('%%')
            else:
                _db_query_tv_episode_id = tvPlayer.idTvEpisode.like('%%')
            # tv episode id end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = tvPlayer.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = tvPlayer.title.desc() 
            if ARG_SORT == 'newest': _db_sort = tvPlayer.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = tvPlayer.addDate.asc()
            # sort end

            # fetch begin
            get_results = tvPlayer.query.filter(and_(or_(_db_query_id, _db_query_title, _db_query_viewKey), _db_query_content_id, _db_query_tv_season_id, _db_query_tv_episode_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(tvPlayer.query.filter(and_(or_(_db_query_id, _db_query_title, _db_query_viewKey), _db_query_content_id, _db_query_tv_season_id, _db_query_tv_episode_id)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('idContent') or not request.args.get('idTvSeason') or not request.args.get('idTvEpisode') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Oynatıcılar', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'idContent': ARG_CONTENT_ID,
                                                                        'idTvSeason': ARG_TV_SEASON_ID,
                                                                        'idTvEpisode': ARG_TV_EPISODE_ID,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }, \
                                                                    content=content, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent) 
        # `tvplayer` table end 

        # `movieplayer` table begin
        if ARG_TABLE == 'movieplayer':

            RET_URL = url_for('adminpanel_v2_list') + '?table=movieplayer&query=*&idContent=*&page=1&sort=newest&list_count=25'

            ARG_CONTENT_ID = request.args.get('idContent', default='*', type=str)

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = moviePlayer.idPlayer.like('%{}%'.format(ARG_QUERY))
                _db_query_title = moviePlayer.title.like('%{}%'.format(ARG_QUERY))
                _db_query_viewKey = moviePlayer.viewKey.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = moviePlayer.idPlayer.like('%%')
                _db_query_title = moviePlayer.title.like('%%')
                _db_query_viewKey = moviePlayer.viewKey.like('%%')
            # query end 

            # content id begin
            if not ARG_CONTENT_ID == "*":
                if content.query.filter_by(idContent=ARG_CONTENT_ID).first():
                    if content.query.filter_by(idContent=ARG_CONTENT_ID).first().type == 'MOVIE':
                        _db_query_content_id = moviePlayer.idContent == '{}'.format(ARG_CONTENT_ID)
                    else:
                        _db_query_content_id = moviePlayer.idContent.like('%%')
                else:
                    _db_query_content_id = moviePlayer.idContent.like('%%')
            else:
                _db_query_content_id = moviePlayer.idContent.like('%%')
            # content id begin

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = moviePlayer.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = moviePlayer.title.desc() 
            if ARG_SORT == 'newest': _db_sort = moviePlayer.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = moviePlayer.addDate.asc()
            # sort end

            # fetch begin
            get_results = moviePlayer.query.filter(and_(or_(_db_query_id, _db_query_title, _db_query_viewKey), _db_query_content_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(moviePlayer.query.filter(and_(or_(_db_query_id, _db_query_title, _db_query_viewKey), _db_query_content_id)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('idContent') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Oynatıcılar', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'idContent': ARG_CONTENT_ID,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }, \
                                                                    content=content) 
        # `movieplayer` table end 

        # `account` table begin
        if ARG_TABLE == 'account':

            RET_URL = url_for('adminpanel_v2_list') + '?table=account&query=*&page=1&sort=newest&list_count=25'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = account.idAccount.like('%{}%'.format(ARG_QUERY))
                _db_query_username = account.username.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = account.idAccount.like('%%')
                _db_query_username = account.username.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = account.username.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = account.username.desc() 
            if ARG_SORT == 'newest': _db_sort = account.signupDate.desc()
            if ARG_SORT == 'oldest': _db_sort = account.signupDate.asc()
            # sort end

            # fetch begin
            get_results = account.query.filter(or_(_db_query_id, _db_query_username)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(account.query.filter(or_(_db_query_id, _db_query_username)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Hesaplar', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `account` table end 

        # `profile` table begin
        if ARG_TABLE == 'profile':

            RET_URL = url_for('adminpanel_v2_list') + '?table=profile&query=*&page=1&sort=newest&list_count=25'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = profile.idProfile.like('%{}%'.format(ARG_QUERY))
                _db_query_username = profile.username.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = profile.idProfile.like('%%')
                _db_query_username = profile.username.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = profile.username.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = profile.username.desc() 
            if ARG_SORT == 'newest': _db_sort = profile.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = profile.addDate.asc()
            # sort end

            # fetch begin
            get_results = profile.query.filter(or_(_db_query_id, _db_query_username)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(profile.query.filter(or_(_db_query_id, _db_query_username)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Profiller', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }, \
                                                                    account=account) 
        # `profile` table end 

        # `cast` table begin
        if ARG_TABLE == 'cast':

            RET_URL = url_for('adminpanel_v2_list') + '?table=cast&query=*&page=1&sort=newest&list_count=25'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = cast.idCast.like('%{}%'.format(ARG_QUERY))
                _db_query_name = cast.name.like('%{}%'.format(ARG_QUERY))
                _db_query_name_url = cast.nameUrl.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = cast.idCast.like('%%')
                _db_query_name = cast.name.like('%%')
                _db_query_name_url = cast.nameUrl.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = cast.name.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = cast.name.desc() 
            if ARG_SORT == 'newest': _db_sort = cast.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = cast.addDate.asc()
            # sort end

            # fetch begin
            get_results = cast.query.filter(or_(_db_query_id, _db_query_name, _db_query_name_url)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(cast.query.filter(or_(_db_query_id, _db_query_name, _db_query_name_url)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Oyuncular', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `cast` table end 

        # `collection` table begin
        if ARG_TABLE == 'collection':

            RET_URL = url_for('adminpanel_v2_list') + '?table=collection&query=*&page=1&sort=newest&list_count=25'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = collection.idCollection.like('%{}%'.format(ARG_QUERY))
                _db_query_title = collection.title.like('%{}%'.format(ARG_QUERY))
                _db_query_title_url = collection.titleUrl.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = collection.idCollection.like('%%')
                _db_query_title = collection.title.like('%%')
                _db_query_title_url = collection.titleUrl.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = collection.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = collection.title.desc() 
            if ARG_SORT == 'newest': _db_sort = collection.addDate.desc()
            if ARG_SORT == 'oldest': _db_sort = collection.addDate.asc()
            # sort end

            # fetch begin
            get_results = collection.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_url)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(collection.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_url)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Koleksiyonlar', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }, \
                                                                    profile=profile) 
        # `collection` table end 

        # `comments' table begin
        if ARG_TABLE == 'moviecomment' or ARG_TABLE == 'tvcomment' or ARG_TABLE == 'tvtitlecomment' or ARG_TABLE == 'castcomment':

            RET_URL = url_for('adminpanel_v2_list') + '?table={}&query=*&page=1&sort=newest&list_count=250'.format(ARG_TABLE)

            if ARG_TABLE == 'moviecomment': _db = movieComment
            if ARG_TABLE == 'tvcomment': _db = tvComment
            if ARG_TABLE == 'tvtitlecomment': _db = tvTitleComment
            if ARG_TABLE == 'castcomment': _db = castComment

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = _db.idComment.like('%{}%'.format(ARG_QUERY))
                _db_query_text = _db.text.like('%{}%'.format(ARG_QUERY))
                _db_query_idAddProfile = _db.idAddProfile.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = _db.idComment.like('%%')
                _db_query_text = _db.text.like('%%')
                _db_query_idAddProfile = _db.idAddProfile.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = _db.text.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = _db.text.desc() 
            if ARG_SORT == 'newest': _db_sort = _db.idComment.asc()
            # sort end

            # fetch begin
            get_results = _db.query.filter(or_(_db_query_id, _db_query_text, _db_query_idAddProfile)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(_db.query.filter(or_(_db_query_id, _db_query_text, _db_query_idAddProfile)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Yorumlar', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }, content=content, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent, cast=cast) 
        # `comments' table end 

        # `lists' table begin
        if ARG_TABLE == 'countrylist' or ARG_TABLE == 'languagelist' or ARG_TABLE == 'moviegenrelist' or ARG_TABLE == 'tvgenrelist':

            RET_URL = url_for('adminpanel_v2_list') + '?table={}&query=*&page=1&sort=newest&list_count=250'.format(ARG_TABLE)

            if ARG_TABLE == 'countrylist': _db = countryList 
            if ARG_TABLE == 'languagelist': _db = languageList 
            if ARG_TABLE == 'moviegenrelist': _db = movieGenreList 
            if ARG_TABLE == 'tvgenrelist': _db = tvGenreList
            
            # query begin
            if not ARG_QUERY == '*':
                if ARG_TABLE == 'countrylist':
                    _db_query_id = _db.idISO_3166_1.like('%{}%'.format(ARG_QUERY))
                if ARG_TABLE == 'languagelist':
                    _db_query_id = _db.idISO_639_1.like('%{}%'.format(ARG_QUERY))
                if ARG_TABLE == 'moviegenrelist':
                    _db_query_id = _db.idGenre.like('%{}%'.format(ARG_QUERY))
                if ARG_TABLE == 'tvgenrelist':
                    _db_query_id = _db.idGenre.like('%{}%'.format(ARG_QUERY))
                _db_query_title = _db.title.like('%{}%'.format(ARG_QUERY))
                _db_query_title_original = _db.titleOriginal.like('%{}%'.format(ARG_QUERY))
            else:
                if ARG_TABLE == 'countrylist': 
                    _db_query_id = _db.idISO_3166_1.like('%%')
                if ARG_TABLE == 'languagelist': 
                    _db_query_id = _db.idISO_639_1.like('%%')
                if ARG_TABLE == 'moviegenrelist': 
                    _db_query_id = _db.idGenre.like('%%')
                if ARG_TABLE == 'tvgenrelist':
                    _db_query_id = _db.idGenre.like('%%')
                _db_query_title = _db.title.like('%%')
                _db_query_title_original = _db.titleOriginal.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = _db.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = _db.title.desc() 
            if ARG_SORT == 'newest': _db_sort = _db.titleOriginal.asc()
            # sort end

            # fetch begin
            get_results = _db.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(_db.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Listeler', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `lists' table end 

        """
        # `countrylist` table begin
        if ARG_TABLE == 'countrylist':

            RET_URL = url_for('adminpanel_v2_list') + '?table=countrylist&query=*&page=1&sort=id&list_count=250'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = countryList.idISO_3166_1.like('%{}%'.format(ARG_QUERY))
                _db_query_title = countryList.title.like('%{}%'.format(ARG_QUERY))
                _db_query_title_original = countryList.titleOriginal.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = countryList.idISO_3166_1.like('%%')
                _db_query_title = countryList.title.like('%%')
                _db_query_title_original = countryList.titleOriginal.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = countryList.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = countryList.title.desc() 
            if ARG_SORT == 'newest': _db_sort = countryList.idISO_3166_1.asc()
            if ARG_SORT == 'id': _db_sort = countryList.idISO_3166_1.asc()
            # sort end

            # fetch begin
            get_results = countryList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(countryList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Ülke Listesi', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `countrylist` table end 

        # `languagelist` table begin
        if ARG_TABLE == 'languagelist':

            RET_URL = url_for('adminpanel_v2_list') + '?table=languagelist&query=*&page=1&sort=id&list_count=250'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = languageList.idISO_639_1.like('%{}%'.format(ARG_QUERY))
                _db_query_title = languageList.title.like('%{}%'.format(ARG_QUERY))
                _db_query_title_original = languageList.titleOriginal.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = languageList.idISO_639_1.like('%%')
                _db_query_title = languageList.title.like('%%')
                _db_query_title_original = languageList.titleOriginal.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = languageList.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = languageList.title.desc() 
            if ARG_SORT == 'newest': _db_sort = languageList.idISO_639_1.asc()
            if ARG_SORT == 'id': _db_sort = languageList.idISO_639_1.asc()
            # sort end

            # fetch begin
            get_results = languageList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(languageList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Dil Listesi', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `languagelist` table end 

        # `moviegenrelist` table begin
        if ARG_TABLE == 'moviegenrelist':

            RET_URL = url_for('adminpanel_v2_list') + '?table=moviegenrelist&query=*&page=1&sort=id&list_count=250'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = movieGenreList.idGenre.like('%{}%'.format(ARG_QUERY))
                _db_query_title = movieGenreList.title.like('%{}%'.format(ARG_QUERY))
                _db_query_title_original = movieGenreList.titleOriginal.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = movieGenreList.idGenre.like('%%')
                _db_query_title = movieGenreList.title.like('%%')
                _db_query_title_original = movieGenreList.titleOriginal.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = movieGenreList.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = movieGenreList.title.desc() 
            if ARG_SORT == 'newest': _db_sort = movieGenreList.idGenre.asc()
            if ARG_SORT == 'id': _db_sort = movieGenreList.idGenre.asc()
            # sort end

            # fetch begin
            get_results = movieGenreList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(movieGenreList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Film Türü Listesi', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `moviegenrelist` table end 

        # `tvgenrelist` table begin
        if ARG_TABLE == 'tvgenrelist':

            RET_URL = url_for('adminpanel_v2_list') + '?table=tvgenrelist&query=*&page=1&sort=id&list_count=250'

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = tvGenreList.idGenre.like('%{}%'.format(ARG_QUERY))
                _db_query_title = tvGenreList.title.like('%{}%'.format(ARG_QUERY))
                _db_query_title_original = tvGenreList.titleOriginal.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = tvGenreList.idGenre.like('%%')
                _db_query_title = tvGenreList.title.like('%%')
                _db_query_title_original = tvGenreList.titleOriginal.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = tvGenreList.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = tvGenreList.title.desc() 
            if ARG_SORT == 'newest': _db_sort = tvGenreList.idGenre.asc()
            if ARG_SORT == 'id': _db_sort = tvGenreList.idGenre.asc()
            # sort end

            # fetch begin
            get_results = tvGenreList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(tvGenreList.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_original)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Dizi Türü Listesi', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    }) 
        # `tvgenrelist` table end 
        """

        # `report' table begin
        if ARG_TABLE == 'report':

            RET_URL = url_for('adminpanel_v2_list') + '?table={}&query=*&page=1&sort=newest&list_count=250'.format(ARG_TABLE)

            # query begin
            if not ARG_QUERY == '*':
                _db_query_id = report.report.idReport.like('%{}%'.format(ARG_QUERY))
                _db_query_name = report.report.name.like('%{}%'.format(ARG_QUERY))
                _db_query_title = report.report.title.like('%{}%'.format(ARG_QUERY))
            else:
                _db_query_id = report.report.idReport.like('%%')
                _db_query_name = report.report.name.like('%%')
                _db_query_title = report.report.title.like('%%')
            # query end 

            # sort begin
            if ARG_SORT == 'a-to-z': _db_sort = report.report.title.asc() 
            if ARG_SORT == 'z-to-a': _db_sort = report.report.title.desc() 
            if ARG_SORT == 'newest': _db_sort = report.report.addDate.desc()
            # sort end

            # fetch begin
            get_results = report.report.query.filter(or_(_db_query_id, _db_query_name, _db_query_title)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
            DEF_PAGE_MAX = ceil(len(report.report.query.filter(or_(_db_query_id, _db_query_name, _db_query_title)).all()) / ARG_LIST_COUNT)
            # fetch end

            # url args validation begin
            if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/list/index.html', title='Raporlar', results_info=get_results, \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'query': ARG_QUERY,
                                                                        'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                                                        'sort': ARG_SORT,
                                                                        'list_count': ARG_LIST_COUNT,
                                                                    })#, content=content, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent, cast=cast) 
        # `report' table end 

        # `test` table begin
        if ARG_TABLE == 'test':
            return render_template('adminpanel_v2/list/index.html', title='İçerikler', results_info='--', \
                                                                    _ARG = {
                                                                        'table': 'test',
                                                                        'query': '*',
                                                                        'page': 1, 'page_max': 100,
                                                                        'sort': 'newest',
                                                                        'list_count': 15,
                                                                    }) 
        # `test` table end 

        # non-exists table begin
        else: return redirect(RET_URL)
        # non-exists table end 
    else: return redirect(RET_URL) 

    return render_template('adminpanel_v2/list/index.html', \
                                        _ARG = {
                                          'table': 'content',
                                          'query': '****',
                                          'page': 1, 'page_max': 100,
                                          'sort': '-',
                                          'list_count': 25,
                                        })
