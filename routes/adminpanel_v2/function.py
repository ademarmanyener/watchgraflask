# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/v2/function/table:<table_name>/function:<function_name>', methods=['POST'])
def adminpanel_v2_function(table_name, function_name):
    if not check_admin(): return make_response(jsonify({'err_msg': 'unvalid permission.'}))
    if not request.is_json: return make_response(jsonify({'err_msg': 'unvalid `JSON`.'}))

    GET_DICTIONARY = request.get_json()['dictionary']

    # content
    if table_name == 'content':
        # DROP
        # DICTIONARY: 'idContent'
        if function_name == 'drop':
            if GET_DICTIONARY['idContent']:
                select_content = content.query.filter_by(idContent=GET_DICTIONARY['idContent']).first()
                select_content.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # IMPORT FROM TMDB
        # DICTIONARY: 'type'['Movie', 'TV'], 'idTmdb'
        if function_name == 'importFromTmdb':
            if GET_DICTIONARY['idTmdb'] and GET_DICTIONARY['type']:
                if GET_DICTIONARY['type'] == 'Movie':
                    # BETA! add this also to another functions, but first test it well.
                    if content.query.filter(and_(content.idTmdb == GET_DICTIONARY['idTmdb'], content.type == 'MOVIE')).first():
                        return make_response(jsonify({'succ_msg': 'OK.'}))
                        #return make_response(jsonify({'err_msg': 'This content with the tmdb_id already exists.'}))

                    TMDBSimpleasy.Movie.addComprehensive(get_tmdb_id=GET_DICTIONARY['idTmdb'])
                    return make_response(jsonify({'succ_msg': 'OK.'}))
                if GET_DICTIONARY['type'] == 'TV':
                    TMDBSimpleasy.TV.addComprehensive(get_tmdb_id=GET_DICTIONARY['idTmdb'])
                    return make_response(jsonify({'succ_msg': 'OK.'}))

        # IMPORT FROM TMDB QUERY
        # DICTIONARY: 'type'['Movie', 'TV'], 'queryTitle'
        if function_name == 'importFromTmdbQuery':
            if GET_DICTIONARY['queryTitle'] and GET_DICTIONARY['type']:
                if GET_DICTIONARY['type'] == 'Movie':
                    list_idTmdb = []
                    list_title = []
                    list_imagePoster = []
                    get_results = tmdb.Search().movie(query=GET_DICTIONARY['queryTitle'])['results']
                    for result in get_results:
                        list_idTmdb.append(result['id'])
                        list_title.append(result['title'])
                        list_imagePoster.append('https://www.themoviedb.org/t/p/w300' + str(result['poster_path']))
                    return make_response(jsonify({'succ_msg': 'OK.', 'list_idTmdb': list_idTmdb, 'list_title': list_title, 'list_imagePoster': list_imagePoster}))
                if GET_DICTIONARY['type'] == 'TV':
                    list_idTmdb = []
                    list_title = []
                    list_imagePoster = []
                    get_results = tmdb.Search().tv(query=GET_DICTIONARY['queryTitle'])['results']
                    for result in get_results:
                        list_idTmdb.append(result['id'])
                        list_title.append(result['name'])
                        list_imagePoster.append('https://www.themoviedb.org/t/p/w300' + str(result['poster_path']))
                    return make_response(jsonify({'succ_msg': 'OK.', 'list_idTmdb': list_idTmdb, 'list_title': list_title, 'list_imagePoster': list_imagePoster}))

        # INSERT NEW
        # DICTIONARY: 'title', 'titleOriginal', 'titleUrl', 'overview'[nullable], 'idTmdb'[nullable], 'idImdb'[nullable], 'type'['MOVIE', 'TV']
        if function_name == 'insertNew':
            if GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal'] and GET_DICTIONARY['titleUrl'] and GET_DICTIONARY['type']:
                db.session.add(content(
                    idAddProfile = session['PROFILE']['idProfile'],
                    idAddAccount = session['ACCOUNT']['idAccount'],
                    type = GET_DICTIONARY['type'],
                    title = GET_DICTIONARY['title'],
                    titleOriginal = GET_DICTIONARY['titleOriginal'],
                    titleUrl = GET_DICTIONARY['titleUrl'],
                    overview = GET_DICTIONARY['overview'],
                    idTmdb = GET_DICTIONARY['idTmdb'],
                    idImdb = GET_DICTIONARY['idImdb'],
                    imagePoster = '/static/img/defaults/poster_content.png',
                    imageBackground = '/static/img/defaults/background_content.png',
                    adult = 0,
                    visibility = 1,
                    voteAverage = 0,
                    releaseDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # FETCH THE POPULARS
        # DICTIONARY: 'type'['MOVIE', 'TV']
        if function_name == 'fetchThePopulars':
            if GET_DICTIONARY['type']:
                if GET_DICTIONARY['type'] == 'MOVIE':
                    get_list = tmdb.Movies().popular(language=TMDB_LANGUAGE)['results']
                    for i in get_list:
                        if not content.query.filter(and_(content.type == 'MOVIE', content.idTmdb == i['id'])).first():
                            TMDBSimpleasy.Movie.addComprehensive(get_tmdb_id=i['id'])
                    return make_response(jsonify({'succ_msg': 'OK.'}))

                if GET_DICTIONARY['type'] == 'TV':
                    get_list = tmdb.TV().popular(language=TMDB_LANGUAGE)['results']
                    for i in get_list:
                        if not content.query.filter(and_(content.type == 'TV', content.idTmdb == i['id'])).first():
                            TMDBSimpleasy.TV.addComprehensive(get_tmdb_id=i['id'])
                    return make_response(jsonify({'succ_msg': 'OK.'}))

                else:
                    return make_response(jsonify({'err_msg': 'Unexpected content type.'}))

        # FETCH THE CLASSICS
        # DICTIONARY: 'type'['MOVIE', 'TV']
        if function_name == 'fetchTheClassics':
            if GET_DICTIONARY['type']:
                if GET_DICTIONARY['type'] == 'MOVIE':
                    get_list = tmdb.Movies().top_rated(language=TMDB_LANGUAGE)['results']
                    for i in get_list:
                        if not content.query.filter(and_(content.type == 'MOVIE', content.idTmdb == i['id'])).first():
                            TMDBSimpleasy.Movie.addComprehensive(get_tmdb_id=i['id'])
                    return make_response(jsonify({'succ_msg': 'OK.'}))

                if GET_DICTIONARY['type'] == 'TV':
                    get_list = tmdb.TV().top_rated(language=TMDB_LANGUAGE)['results']
                    for i in get_list:
                        if not content.query.filter(and_(content.type == 'TV', content.idTmdb == i['id'])).first():
                            TMDBSimpleasy.TV.addComprehensive(get_tmdb_id=i['id'])
                    return make_response(jsonify({'succ_msg': 'OK.'}))

                else:
                    return make_response(jsonify({'err_msg': 'Unexpected content type.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # tvseasoncontent
    if table_name == 'tvseasoncontent':
        # DROP
        # DICTIONARY: 'idTvSeason'
        if function_name == 'drop':
            if GET_DICTIONARY['idTvSeason']:
                select_tvseasoncontent = tvSeasonContent.query.filter_by(idTvSeason=GET_DICTIONARY['idTvSeason']).first()
                select_tvseasoncontent.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # IMPORT FROM TMDB
        # DICTIONARY: 'seasonNumber', 'idTmdb'
        if function_name == 'importFromTmdb':
            if GET_DICTIONARY['idTmdb'] and GET_DICTIONARY['seasonNumber']:
                TMDBSimpleasy.TV.addSeason(get_tmdb_id=GET_DICTIONARY['idTmdb'], get_season_number=GET_DICTIONARY['seasonNumber'])
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'title', 'overview'[nullable], 'idTmdb'[nullable], 'seasonNumber', 'airDate'[nullable]
        if function_name == 'insertNew':
            if GET_DICTIONARY['title'] and GET_DICTIONARY['seasonNumber']:
                db.session.add(tvSeasonContent(
                    idContent = content.query.filter_by(idTmdb=GET_DICTIONARY['idTmdb']).first().idContent,
                    idAddProfile = session['PROFILE']['idProfile'],
                    idAddAccount = session['ACCOUNT']['idAccount'],
                    title = GET_DICTIONARY['title'],
                    overview = GET_DICTIONARY['overview'],
                    idTmdb = GET_DICTIONARY['idTmdb'],
                    imagePoster = '/static/img/defaults/poster_season.png',
                    seasonNumber = GET_DICTIONARY['seasonNumber'],
                    visibility = 1,
                    airDate = GET_DICTIONARY['airDate'],
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # tvepisodecontent
    if table_name == 'tvepisodecontent':
        # DROP
        # DICTIONARY: 'idTvEpisode'
        if function_name == 'drop':
            if GET_DICTIONARY['idTvEpisode']:
                select_tvepisodecontent = tvEpisodeContent.query.filter_by(idTvEpisode=GET_DICTIONARY['idTvEpisode']).first()
                select_tvepisodecontent.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # IMPORT FROM TMDB
        # DICTIONARY: 'seasonNumber', 'episodeNumber', 'idTmdb'
        if function_name == 'importFromTmdb':
            if GET_DICTIONARY['idTmdb'] and GET_DICTIONARY['seasonNumber'] and GET_DICTIONARY['episodeNumber']:
                TMDBSimpleasy.TV.addEpisode(get_tmdb_id=GET_DICTIONARY['idTmdb'], get_season_number=GET_DICTIONARY['seasonNumber'], get_episode_number=GET_DICTIONARY['episodeNumber'])
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'title', 'overview'[nullable], 'idTmdb'[nullable], 'idImdb'[nullable], 'seasonNumber', 'episodeNumber', 'airDate'[nullable]
        if function_name == 'insertNew':
            if GET_DICTIONARY['title'] and GET_DICTIONARY['seasonNumber'] and GET_DICTIONARY['episodeNumber']:
                db.session.add(tvEpisodeContent(
                    idContent = content.query.filter_by(idTmdb=GET_DICTIONARY['idTmdb']).first().idContent,
                    idTvSeason = tvSeasonContent.query.filter_by(idTmdb=GET_DICTIONARY['idTmdb']).first().idTvSeason,
                    idAddProfile = session['PROFILE']['idProfile'],
                    idAddAccount = session['ACCOUNT']['idAccount'],
                    title = GET_DICTIONARY['title'],
                    overview = GET_DICTIONARY['overview'],
                    idTmdb = GET_DICTIONARY['idTmdb'],
                    idImdb = GET_DICTIONARY['idImdb'],
                    imagePoster = '/static/img/defaults/poster_episode.png',
                    seasonNumber = GET_DICTIONARY['seasonNumber'],
                    episodeNumber = GET_DICTIONARY['episodeNumber'],
                    visibility = 1,
                    voteAverage = 0,
                    airDate = GET_DICTIONARY['airDate'],
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # tvplayer
    if table_name == 'tvplayer':
        # DROP
        # DICTIONARY: 'idPlayer'
        if function_name == 'drop':
            if GET_DICTIONARY['idPlayer']:
                select_tvplayer = tvPlayer.query.filter_by(idPlayer=GET_DICTIONARY['idPlayer']).first()
                select_tvplayer.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'title', 'source', 'order', 'seasonNumber', 'episodeNumber', 'language', 'type'
        if function_name == 'insertNew':
            if GET_DICTIONARY['title'] and GET_DICTIONARY['source'] and GET_DICTIONARY['order'] and GET_DICTIONARY['seasonNumber'] and GET_DICTIONARY['episodeNumber'] and GET_DICTIONARY['language'] and GET_DICTIONARY['type']:
                db.session.add(tvPlayer(
                    idContent = GET_DICTIONARY['_ARG']['idContent'],
                    idTvSeason = GET_DICTIONARY['_ARG']['idTvSeason'],
                    idTvEpisode = GET_DICTIONARY['_ARG']['idTvEpisode'],
                    idAddProfile = session['PROFILE']['idProfile'],
                    idAddAccount = session['ACCOUNT']['idAccount'],
                    language = GET_DICTIONARY['language'],
                    source = GET_DICTIONARY['source'],
                    title = GET_DICTIONARY['title'],
                    type = GET_DICTIONARY['type'],
                    visibility = 1,
                    order = GET_DICTIONARY['order'],
                    seasonNumber = GET_DICTIONARY['seasonNumber'],
                    episodeNumber = GET_DICTIONARY['episodeNumber'],
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # movieplayer
    if table_name == 'movieplayer':
        # DROP
        # DICTIONARY: 'idPlayer'
        if function_name == 'drop':
            if GET_DICTIONARY['idPlayer']:
                make_response(jsonify({'succ_msg': 'işlem başladı.'}))
                select_movieplayer = moviePlayer.query.filter_by(idPlayer=GET_DICTIONARY['idPlayer']).first()
                select_movieplayer.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'title', 'source', 'order', 'language', 'type'
        if function_name == 'insertNew':
            if GET_DICTIONARY['title'] and GET_DICTIONARY['source'] and GET_DICTIONARY['order'] and GET_DICTIONARY['language'] and GET_DICTIONARY['type']:
                db.session.add(moviePlayer(
                    idContent = GET_DICTIONARY['_ARG']['idContent'],
                    idAddProfile = session['PROFILE']['idProfile'],
                    idAddAccount = session['ACCOUNT']['idAccount'],
                    language = GET_DICTIONARY['language'],
                    source = GET_DICTIONARY['source'],
                    title = GET_DICTIONARY['title'],
                    type = GET_DICTIONARY['type'],
                    visibility = 1,
                    order = GET_DICTIONARY['order'],
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # account 
    if table_name == 'account':
        # DROP
        # DICTIONARY: 'idAccount'
        if function_name == 'drop':
            if GET_DICTIONARY['idAccount']:
                select_account = account.query.filter_by(idAccount=GET_DICTIONARY['idAccount']).first()
                select_account.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'username', 'emailAddress', 'password', 'securityPassword'
        if function_name == 'insertNew':
            if GET_DICTIONARY['username'] and GET_DICTIONARY['emailAddress'] and GET_DICTIONARY['password'] and GET_DICTIONARY['securityPassword']:
                db.session.add(account(
                    username = GET_DICTIONARY['username'],
                    emailAddress = GET_DICTIONARY['emailAddress'],
                    password = hash_str_hash(get_str=GET_DICTIONARY['password']),
                    securityPassword =  hash_str_hash(get_str=GET_DICTIONARY['securityPassword']),
                    permission = 'USER',
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # profile 
    if table_name == 'profile':
        # DROP
        # DICTIONARY: 'idProfile'
        if function_name == 'drop':
            if GET_DICTIONARY['idProfile']:
                select_profile = profile.query.filter_by(idProfile=GET_DICTIONARY['idProfile']).first()
                select_profile.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'idAccount', 'username', 'password'[nullable], 'biography'[nullable], 'adult'['0', '1'], 'permission'['USER', 'ADMIN'], 'private'['0', '1']
        if function_name == 'insertNew':
            if GET_DICTIONARY['idAccount'] and GET_DICTIONARY['username'] and GET_DICTIONARY['adult'] and GET_DICTIONARY['permission'] and GET_DICTIONARY['private']:
                if account.query.filter_by(idAccount=GET_DICTIONARY['idAccount']).first():
                    db.session.add(profile(
                        idAccount = GET_DICTIONARY['idAccount'],
                        username = GET_DICTIONARY['username'],
                        password = GET_DICTIONARY['password'],
                        biography = GET_DICTIONARY['biography'],
                        adult =  GET_DICTIONARY['adult'],
                        permission =  GET_DICTIONARY['permission'],
                        private =  GET_DICTIONARY['private'],
                        imageAvatar = '/static/img/default_image_avatar.png',
                        imageBackground = '/static/img/default_image_background.jpg',
                        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE))
                    ))
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'OK.'}))
            else: make_response(jsonify({'err_msg': 'noep.'}))

        # INSERT NEW QUERY
        # DICTIONARY: 'queryProfile'
        if function_name == 'insertNewQuery':
            if GET_DICTIONARY['queryAccount']:
                list_idAccount = []
                list_username = []
                list_permission = []
                get_results = account.query.filter(or_(account.idAccount.like('%{}%'.format(GET_DICTIONARY['queryAccount'])), account.username.like('%{}%'.format(GET_DICTIONARY['queryAccount'])))).order_by(account.username.asc()).limit(25).all()
                for result in get_results:
                    list_idAccount.append(result.idAccount)
                    list_username.append(result.username)
                    list_permission.append(result.permission)
                return make_response(jsonify({'succ_msg': 'OK.', 'list_idAccount': list_idAccount, 'list_username': list_username, 'list_permission': list_permission}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # cast
    if table_name == 'cast':
        # DROP
        # DICTIONARY: 'idCast'
        if function_name == 'drop':
            if GET_DICTIONARY['idCast']:
                select_cast = cast.query.filter_by(idCast=GET_DICTIONARY['idCast']).first()
                select_cast.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # IMPORT FROM TMDB
        # DICTIONARY: 'idTmdb'
        if function_name == 'importFromTmdb':
            TMDBSimpleasy.Cast.addCast(get_tmdb_id=GET_DICTIONARY['idTmdb'])
            return make_response(jsonify({'succ_msg': 'OK.'}))

        # IMPORT FROM TMDB QUERY
        # DICTIONARY: 'queryName'
        if function_name == 'importFromTmdbQuery':
            if GET_DICTIONARY['queryName']:
                list_idTmdb = []
                list_name = []
                list_imagePoster = []
                get_results = tmdb.Search().person(query=GET_DICTIONARY['queryName'])['results']
                for result in get_results:
                    list_idTmdb.append(result['id'])
                    list_name.append(result['name'])
                    list_imagePoster.append('https://www.themoviedb.org/t/p/w300' + str(result['profile_path']))
                return make_response(jsonify({'succ_msg': 'OK.', 'list_idTmdb': list_idTmdb, 'list_name': list_name, 'list_imagePoster': list_imagePoster}))

        # INSERT NEW
        # DICTIONARY: 'gender', 'name', 'nameUrl', 'biography'[nullable], 'idTmdb', 'idImdb', 'idTwitter'[nullable], 'idInstagram'[nullable], 'adult'[0, 1], 'birthPlace'[nullable], 'birthDate'[nullable], 'deathDate'[nullable]
        if function_name == 'insertNew':
            if GET_DICTIONARY['gender'] and GET_DICTIONARY['name'] and GET_DICTIONARY['nameUrl'] and GET_DICTIONARY['idTmdb'] and GET_DICTIONARY['idImdb'] and GET_DICTIONARY['adult']:
                db.session.add(cast(
                    idAddProfile = session['PROFILE']['idProfile'],
                    idAddAccount = session['ACCOUNT']['idAccount'],
                    gender = GET_DICTIONARY['gender'],
                    name = GET_DICTIONARY['name'],
                    nameUrl = GET_DICTIONARY['nameUrl'],
                    biography = GET_DICTIONARY['biography'],
                    idTmdb = GET_DICTIONARY['idTmdb'],
                    idImdb = GET_DICTIONARY['idImdb'],
                    idTwitter = GET_DICTIONARY['idTwitter'],
                    idInstagram = GET_DICTIONARY['idInstagram'],
                    imagePoster = '/static/img/defaults/poster_cast.png',
                    adult = GET_DICTIONARY['adult'],
                    visibility = 1,
                    birthPlace = GET_DICTIONARY['birthPlace'],
                    birthDate = GET_DICTIONARY['birthDate'],
                    deathDate = GET_DICTIONARY['deathDate'],
                    lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # collection
    if table_name == 'collection':
        # DROP
        # DICTIONARY: 'idCollection'
        if function_name == 'drop':
            if GET_DICTIONARY['idCollection']:
                select_collection = collection.query.filter_by(idCollection=GET_DICTIONARY['idCollection']).first()
                select_collection.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'idAddProfile', 'title', 'titleUrl', 'overview'[nullable], 'private'['0', '1'], 'recommended'['0', '1']
        if function_name == 'insertNew':
            if GET_DICTIONARY['idAddProfile'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleUrl'] and GET_DICTIONARY['private'] and GET_DICTIONARY['recommended']:
                if profile.query.filter_by(idProfile=GET_DICTIONARY['idAddProfile']).first():
                    db.session.add(collection(
                        idAddProfile = GET_DICTIONARY['idAddProfile'],
                        idAddAccount = profile.query.filter_by(idProfile=GET_DICTIONARY['idAddProfile']).first().idAccount,
                        title = GET_DICTIONARY['title'],
                        titleUrl = GET_DICTIONARY['titleUrl'],
                        overview = GET_DICTIONARY['overview'],
                        private = GET_DICTIONARY['private'],
                        imagePoster = '/static/img/defaults/poster_collection.png',
                        imageBackground = '/static/img/defaults/background_collection.png',
                        recommended = GET_DICTIONARY['recommended'],
                        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
                    ))
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW QUERY
        # DICTIONARY: 'queryProfile'
        if function_name == 'insertNewQuery':
            if GET_DICTIONARY['queryProfile']:
                list_idProfile = []
                list_username = []
                list_username_of_account = []
                list_imageAvatar = []
                get_results = profile.query.filter(or_(profile.idProfile.like('%{}%'.format(GET_DICTIONARY['queryProfile'])), profile.username.like('%{}%'.format(GET_DICTIONARY['queryProfile'])))).order_by(profile.username.asc()).limit(25).all()
                for result in get_results:
                    list_idProfile.append(result.idProfile)
                    list_username.append(result.username)
                    list_username_of_account.append(account.query.filter_by(idAccount=result.idAccount).first().username)
                    list_imageAvatar.append(result.imageAvatar)
                return make_response(jsonify({'succ_msg': 'OK.', 'list_idProfile': list_idProfile, 'list_username': list_username, 'list_username_of_account': list_username_of_account, 'list_imageAvatar': list_imageAvatar}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # comments ['moviecomment', 'tvcomment', 'tvtitlecomment', 'castcomment']
    if table_name == 'comments':
        # DROP
        # DICTIONARY: 'idComment', 'table'
        if function_name == 'drop':
            if GET_DICTIONARY['idComment'] and GET_DICTIONARY['table']:
                if GET_DICTIONARY['table'] == 'moviecomment': _db = movieComment
                if GET_DICTIONARY['table'] == 'tvcomment': _db = tvComment
                if GET_DICTIONARY['table'] == 'tvtitlecomment': _db = tvTitleComment
                if GET_DICTIONARY['table'] == 'castcomment': _db = castComment
                select_comment = _db.query.filter_by(idComment=GET_DICTIONARY['idComment']).first()
                select_comment.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # UPDATE RECORD 
        # DICTIONARY: 'idComment', 'text', 'table'
        if function_name == 'updateRecord':
            if GET_DICTIONARY['idComment'] and GET_DICTIONARY['text'] and GET_DICTIONARY['table']:
                if GET_DICTIONARY['table'] == 'moviecomment': _db = movieComment
                if GET_DICTIONARY['table'] == 'tvcomment': _db = tvComment
                if GET_DICTIONARY['table'] == 'tvtitlecomment': _db = tvTitleComment
                if GET_DICTIONARY['table'] == 'castcomment': _db = castComment
                get_comment = _db.query.filter_by(idComment=GET_DICTIONARY['idComment']).first()
                if get_comment:
                    get_comment.text = GET_DICTIONARY['text']
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'Kayıt başarıyla güncellendi.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    """
    # BETA
    # lists ['countrylist', 'languagelist', 'moviegenrelist', 'tvgenrelist']
    if table_name == 'lists':
        # DROP
        # DICTIONARY: ['idISO_3166_1', 'idISO_639_1', 'idGenre', 'idGenre'], 'table'['countrylist', 'languagelist', 'moviegenrelist', 'tvgenrelist']
        if function_name == 'drop':
            if GET_DICTIONARY['table']:
                if GET_DICTIONARY['table'] == 'countrylist':
                    select_list = countryList.query.filter_by(idISO_3166_1=GET_DICTIONARY['idISO_3166_1']).first()
                if GET_DICTIONARY['table'] == 'languagelist':
                    select_list = languageList.query.filter_by(idISO_3166_1=GET_DICTIONARY['idISO_639_1']).first()
                if GET_DICTIONARY['table'] == 'moviegenrelist':
                    select_list = movieGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                if GET_DICTIONARY['table'] == 'tvgenrelist':
                    select_list = tvGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                select_list.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: ['idISO_3166_1', 'idISO_639_1', 'idGenre', 'idGenre'], 'table'['countrylist', 'languagelist', 'moviegenrelist', 'tvgenrelist'], 'title', 'titleOriginal'
        if function_name == 'insertNew':
            if GET_DICTIONARY['table'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                if GET_DICTIONARY['table'] == 'countrylist':
                    db.session.add(countryList(
                        idISO_3166_1 = GET_DICTIONARY['idISO_3166_1'],
                        title = GET_DICTIONARY['title'],
                        titleOriginal = GET_DICTIONARY['titleOriginal'],
                    ))
                if GET_DICTIONARY['table'] == 'languagelist':
                    db.session.add(languageList(
                        idISO_639_1 = GET_DICTIONARY['idISO_639_1'],
                        title = GET_DICTIONARY['title'],
                        titleOriginal = GET_DICTIONARY['titleOriginal'],
                    ))
                if GET_DICTIONARY['table'] == 'moviegenrelist':
                    db.session.add(movieGenreList(
                        idGenre = GET_DICTIONARY['idGenre'],
                        title = GET_DICTIONARY['title'],
                        titleOriginal = GET_DICTIONARY['titleOriginal'],
                    ))
                if GET_DICTIONARY['table'] == 'tvgenrelist':
                    db.session.add(tvGenreList(
                        idGenre = GET_DICTIONARY['idGenre'],
                        title = GET_DICTIONARY['title'],
                        titleOriginal = GET_DICTIONARY['titleOriginal'],
                    ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # UPDATE RECORD 
        # DICTIONARY: ['idISO_3166_1', 'idISO_639_1', 'idGenre', 'idGenre'], 'table'['countrylist', 'languagelist', 'moviegenrelist', 'tvgenrelist'], 'title', 'titleOriginal'
        if function_name == 'updateRecord':
            if GET_DICTIONARY['table'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                if GET_DICTIONARY['table'] == 'countrylist':
                    select_list = countryList.query.filter_by(idISO_3166_1=GET_DICTIONARY['idISO_3166_1']).first()
                if GET_DICTIONARY['table'] == 'languagelist':
                    select_list = languageList.query.filter_by(idISO_3166_1=GET_DICTIONARY['idISO_639_1']).first()
                if GET_DICTIONARY['table'] == 'moviegenrelist':
                    select_list = movieGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                if GET_DICTIONARY['table'] == 'tvgenrelist':
                    select_list = tvGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                if select_list:
                    get_countrylist.title = GET_DICTIONARY['title']
                    get_countrylist.titleOriginal = GET_DICTIONARY['titleOriginal']
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'Kayıt başarıyla güncellendi.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))
    """

    # countrylist
    if table_name == 'countrylist':
        # DROP
        # DICTIONARY: 'idISO_3166_1'
        if function_name == 'drop':
            if GET_DICTIONARY['idISO_3166_1']:
                select_countrylist = countryList.query.filter_by(idISO_3166_1=GET_DICTIONARY['idISO_3166_1']).first()
                select_countrylist.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'idISO_3166_1', 'title', 'titleOriginal'
        if function_name == 'insertNew':
            if GET_DICTIONARY['idISO_3166_1'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                db.session.add(countryList(
                    idISO_3166_1 = GET_DICTIONARY['idISO_3166_1'],
                    title = GET_DICTIONARY['title'],
                    titleOriginal = GET_DICTIONARY['titleOriginal'],
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # UPDATE RECORD 
        # DICTIONARY: 'idISO_3166_1', 'title', 'titleOriginal'
        if function_name == 'updateRecord':
            if GET_DICTIONARY['idISO_3166_1'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                get_countrylist = countryList.query.filter_by(idISO_3166_1=GET_DICTIONARY['idISO_3166_1']).first()
                if get_countrylist:
                    get_countrylist.title = GET_DICTIONARY['title']
                    get_countrylist.titleOriginal = GET_DICTIONARY['titleOriginal']
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'Kayıt başarıyla güncellendi.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # languagelist
    if table_name == 'languagelist':
        # DROP
        # DICTIONARY: 'idISO_639_1'
        if function_name == 'drop':
            if GET_DICTIONARY['idISO_639_1']:
                select_languagelist = languageList.query.filter_by(idISO_639_1=GET_DICTIONARY['idISO_639_1']).first()
                select_languagelist.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'idISO_639_1', 'title', 'titleOriginal'
        if function_name == 'insertNew':
            if GET_DICTIONARY['idISO_639_1'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                db.session.add(languageList(
                    idISO_639_1 = GET_DICTIONARY['idISO_639_1'],
                    title = GET_DICTIONARY['title'],
                    titleOriginal = GET_DICTIONARY['titleOriginal'],
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # UPDATE RECORD 
        # DICTIONARY: 'idISO_639_1', 'title', 'titleOriginal'
        if function_name == 'updateRecord':
            if GET_DICTIONARY['idISO_639_1'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                get_languagelist = languageList.query.filter_by(idISO_639_1=GET_DICTIONARY['idISO_639_1']).first()
                if get_languagelist:
                    get_languagelist.title = GET_DICTIONARY['title']
                    get_languagelist.titleOriginal = GET_DICTIONARY['titleOriginal']
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'Kayıt başarıyla güncellendi.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # moviegenrelist
    if table_name == 'moviegenrelist':
        # DROP
        # DICTIONARY: 'idGenre'
        if function_name == 'drop':
            if GET_DICTIONARY['idGenre']:
                select_moviegenrelist = movieGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                select_moviegenrelist.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'idGenre', 'title', 'titleOriginal'
        if function_name == 'insertNew':
            if GET_DICTIONARY['idGenre'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                db.session.add(movieGenreList(
                    idGenre = GET_DICTIONARY['idGenre'],
                    title = GET_DICTIONARY['title'],
                    titleOriginal = GET_DICTIONARY['titleOriginal'],
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # UPDATE RECORD 
        # DICTIONARY: 'idGenre', 'title', 'titleOriginal'
        if function_name == 'updateRecord':
            if GET_DICTIONARY['idGenre'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                get_moviegenrelist = movieGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                if get_moviegenrelist:
                    get_moviegenrelist.title = GET_DICTIONARY['title']
                    get_moviegenrelist.titleOriginal = GET_DICTIONARY['titleOriginal']
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'Kayıt başarıyla güncellendi.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # tvgenrelist
    if table_name == 'tvgenrelist':
        # DROP
        # DICTIONARY: 'idGenre'
        if function_name == 'drop':
            if GET_DICTIONARY['idGenre']:
                select_tvgenrelist = tvGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                select_tvgenrelist.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # INSERT NEW
        # DICTIONARY: 'idGenre', 'title', 'titleOriginal'
        if function_name == 'insertNew':
            if GET_DICTIONARY['idGenre'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                db.session.add(tvGenreList(
                    idGenre = GET_DICTIONARY['idGenre'],
                    title = GET_DICTIONARY['title'],
                    titleOriginal = GET_DICTIONARY['titleOriginal'],
                ))
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # UPDATE RECORD 
        # DICTIONARY: 'idGenre', 'title', 'titleOriginal'
        if function_name == 'updateRecord':
            if GET_DICTIONARY['idGenre'] and GET_DICTIONARY['title'] and GET_DICTIONARY['titleOriginal']:
                get_tvgenrelist = tvGenreList.query.filter_by(idGenre=GET_DICTIONARY['idGenre']).first()
                if get_tvgenrelist:
                    get_tvgenrelist.title = GET_DICTIONARY['title']
                    get_tvgenrelist.titleOriginal = GET_DICTIONARY['titleOriginal']
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'Kayıt başarıyla güncellendi.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # report
    if table_name == 'report':
        # DROP
        # DICTIONARY: 'idReport'
        if function_name == 'drop':
            if GET_DICTIONARY['idReport']:
                select_report = report.report.query.filter_by(idReport=GET_DICTIONARY['idReport']).first()
                select_report.drop()
                return make_response(jsonify({'succ_msg': 'OK.'}))

        # UPDATE RECORD 
        # DICTIONARY: 'idReport', 'name', 'emailAddress', 'title', 'message'
        if function_name == 'updateRecord':
            if GET_DICTIONARY['idReport'] and GET_DICTIONARY['name'] and GET_DICTIONARY['emailAddress'] and GET_DICTIONARY['title'] and GET_DICTIONARY['message']:
                get_report = report.report.query.filter_by(idReport=GET_DICTIONARY['idReport']).first()
                if get_report:
                    get_report.name = GET_DICTIONARY['name']
                    get_report.emailAddress = GET_DICTIONARY['emailAddress']
                    get_report.title = GET_DICTIONARY['title']
                    get_report.message = GET_DICTIONARY['message']
                    db.session.commit()
                    return make_response(jsonify({'succ_msg': 'Kayıt başarıyla güncellendi.'}))

        # ELSE (throw an error)
        else: return make_response(jsonify({'err_msg': 'unvalid `function_name`.'}))

    # ELSE (throw an error)
    else: return make_response(jsonify({'err_msg': 'unvalid `table_name`.'}))
