# -*- encoding: utf-8 -*-
from includes import *

class CustomFormComponent:
    def upload_file(upload_file, save_folder_path):
        _tmp_secureFilename = secure_filename(upload_file.filename)
        _tmp_generatedFilename = str(id_generator(size=32)) + '.' + str(_tmp_secureFilename.split('.')[1])
        upload_file.save(os.path.join(save_folder_path, _tmp_generatedFilename)) 
        try: UploadImageResize(image=os.path.join(save_folder_path, _tmp_generatedFilename)).resize_and_save()
        except: pass
        return

@app.route('/adminpanel/v2/edit/table:<table_name>/id:<id_key>/delete_file/file:<file_name>')
def adminpanel_v2_edit_delete_file(table_name, id_key, file_name):
    if not check_admin(): return redirect(url_for('home'))

    _tmp_filePath = os.path.join(app.root_path, 'storage', table_name, id_key, file_name)
    os.remove(_tmp_filePath)

    return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

@app.route('/adminpanel/v2/edit/table:<table_name>/id:<id_key>/save/', methods=['POST', 'GET'])
def adminpanel_v2_edit_save(table_name, id_key):
    if not check_admin(): return redirect(url_for('home'))

    if request.method == 'POST':
        #### CONTENT EDIT BEGIN
        if table_name == 'content':
            # get db row 
            get_content = content.query.filter_by(idContent=id_key).first()
            if not get_content: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # check if a file is uploaded
            uploadFile = request.files['uploadFile']
            if uploadFile:
                CustomFormComponent.upload_file(upload_file=uploadFile, save_folder_path=os.path.join(app.root_path, 'storage', 'content', get_content.idContent))
                return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

            # get form datas
            GET_FORM_DATA = {
                'title': request.form['input___title'],
                'titleOriginal': request.form['input___titleOriginal'],
                'titleUrl': request.form['input___titleUrl'],
                'overview': request.form['input___overview'],
                'voteAverage': request.form['input___voteAverage'],
                'idTmdb': request.form['input___idTmdb'],
                'idImdb': request.form['input___idImdb'],
                'countries': request.form.getlist('select2___country'),
                'languages': request.form.getlist('select2___language'),
                'genres': request.form.getlist('select2___genre'),
                'imagePoster': request.form['input___imagePoster'],
                'imageBackground': request.form['input___imageBackground'],
                'releaseDate': request.form['input___releaseDate'],
                'adult': request.form['select2___adult'],
                'visibility': request.form['select2___visibility'],
                'type': request.form['select2___type'],
            }

            get_content.title = GET_FORM_DATA['title']
            get_content.titleOriginal = GET_FORM_DATA['titleOriginal']
            get_content.titleUrl = GET_FORM_DATA['titleUrl']
            get_content.overview = GET_FORM_DATA['overview']
            get_content.voteAverage = GET_FORM_DATA['voteAverage']
            get_content.idTmdb = GET_FORM_DATA['idTmdb']
            get_content.idImdb = GET_FORM_DATA['idImdb']
            ### array values begin
            ## since the genre, country and the language values're
            ## list, we need to handle with them in a different way
            # first drop all the values
            for get_content_country in contentCountry.query.filter_by(idContent=get_content.idContent).all():
                get_content_country.drop()
            for get_content_language in contentLanguage.query.filter_by(idContent=get_content.idContent).all():
                get_content_language.drop()
            if get_content.type == 'MOVIE':
                _tmp_genreTable = movieContentGenre
            if get_content.type == 'TV':
                _tmp_genreTable = tvContentGenre
            for get_content_genre in _tmp_genreTable.query.filter_by(idContent=get_content.idContent).all():
                get_content_genre.drop()
            # then add the new ones
            for get_country in GET_FORM_DATA['countries']:
                db.session.add(contentCountry(idContent=get_content.idContent, idISO_3166_1=get_country))
            for get_language in GET_FORM_DATA['languages']:
                db.session.add(contentLanguage(idContent=get_content.idContent, idISO_639_1=get_language))
            for get_genre in GET_FORM_DATA['genres']:
                db.session.add(_tmp_genreTable(idContent=get_content.idContent, idGenre=get_genre))
            ### array values end 
            get_content.imagePoster = GET_FORM_DATA['imagePoster']
            get_content.imageBackground = GET_FORM_DATA['imageBackground']
            get_content.releaseDate = GET_FORM_DATA['releaseDate']
            get_content.adult = GET_FORM_DATA['adult']
            get_content.visibility = GET_FORM_DATA['visibility']
            get_content.type = GET_FORM_DATA['type']
        #### CONTENT EDIT END 

        #### TV SEASON CONTENT EDIT BEGIN 
        if table_name == 'tvseasoncontent':
            # get db row 
            get_tvSeasonContent = tvSeasonContent.query.filter_by(idTvSeason=id_key).first()
            if not get_tvSeasonContent: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # check if a file is uploaded
            uploadFile = request.files['uploadFile']
            if uploadFile:
                CustomFormComponent.upload_file(upload_file=uploadFile, save_folder_path=os.path.join(app.root_path, 'storage', 'content', get_tvSeasonContent.idContent))
                return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

            # get form datas
            GET_FORM_DATA = {
                'title': request.form['input___title'],
                'overview': request.form['input___overview'],
                'idTmdb': request.form['input___idTmdb'],
                'imagePoster': request.form['input___imagePoster'],
                #'seasonNumber': request.form['input___seasonNumber'],
                'visibility': request.form['select2___visibility'],
                'airDate': request.form['input___airDate'],
            }

            get_tvSeasonContent.title = GET_FORM_DATA['title']
            get_tvSeasonContent.overview = GET_FORM_DATA['overview']
            get_tvSeasonContent.idTmdb = GET_FORM_DATA['idTmdb']
            get_tvSeasonContent.imagePoster = GET_FORM_DATA['imagePoster']
            #get_tvSeasonContent.seasonNumber = GET_FORM_DATA['seasonNumber']
            get_tvSeasonContent.visibility = GET_FORM_DATA['visibility']
            get_tvSeasonContent.airDate = GET_FORM_DATA['airDate']
        #### TV SEASON CONTENT EDIT END 

        #### TV EPISODE CONTENT EDIT BEGIN 
        if table_name == 'tvepisodecontent':
            # get db row 
            get_tvEpisodeContent = tvEpisodeContent.query.filter_by(idTvEpisode=id_key).first()
            if not get_tvEpisodeContent: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # check if a file is uploaded
            uploadFile = request.files['uploadFile']
            if uploadFile:
                CustomFormComponent.upload_file(upload_file=uploadFile, save_folder_path=os.path.join(app.root_path, 'storage', 'content', get_tvEpisodeContent.idContent))
                return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

            # get form datas
            GET_FORM_DATA = {
                'title': request.form['input___title'],
                'overview': request.form['input___overview'],
                'idTmdb': request.form['input___idTmdb'],
                'idImdb': request.form['input___idImdb'],
                'imagePoster': request.form['input___imagePoster'],
                #'seasonNumber': request.form['input___seasonNumber'],
                #'episodeNumber': request.form['input___episodeNumber'],
                'visibility': request.form['select2___visibility'],
                'voteAverage': request.form['input___voteAverage'],
                'airDate': request.form['input___airDate'],
            }

            get_tvEpisodeContent.title = GET_FORM_DATA['title']
            get_tvEpisodeContent.overview = GET_FORM_DATA['overview']
            get_tvEpisodeContent.idTmdb = GET_FORM_DATA['idTmdb']
            get_tvEpisodeContent.idImdb = GET_FORM_DATA['idImdb']
            get_tvEpisodeContent.imagePoster = GET_FORM_DATA['imagePoster']
            #get_tvEpisodeContent.seasonNumber = GET_FORM_DATA['seasonNumber']
            #get_tvEpisodeContent.episodeNumber = GET_FORM_DATA['episodeNumber']
            get_tvEpisodeContent.visibility = GET_FORM_DATA['visibility']
            get_tvEpisodeContent.voteAverage = GET_FORM_DATA['voteAverage']
            get_tvEpisodeContent.airDate = GET_FORM_DATA['airDate']
        #### TV EPISODE CONTENT EDIT END 

        #### [MOVIE PLAYER, TV PLAYER] EDIT BEGIN 
        if table_name == 'movieplayer' or table_name == 'tvplayer':
            # get db row 
            if table_name == 'movieplayer': _table = moviePlayer
            if table_name == 'tvplayer': _table = tvPlayer
            get_player = _table.query.filter_by(idPlayer=id_key).first()
            if not get_player: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # check if a file is uploaded
            uploadFile = request.files['uploadFile']
            if uploadFile:
                CustomFormComponent.upload_file(upload_file=uploadFile, save_folder_path=os.path.join(app.root_path, 'storage', 'content', get_player.idContent))
                return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

            # get form datas
            GET_FORM_DATA = {
                'title': request.form['input___title'],
                'viewKey': request.form['input___viewKey'],
                'source': request.form['input___source'],
                'order': request.form['input___order'],
                #'seasonNumber': request.form['input___seasonNumber'],
                #'episodeNumber': request.form['input___episodeNumber'],
                'language': request.form['select2___language'],
                'visibility': request.form['select2___visibility'],
                'type': request.form['select2___type'],
            }

            get_player.title = GET_FORM_DATA['title']
            get_player.viewKey = GET_FORM_DATA['viewKey']
            get_player.source = GET_FORM_DATA['source']
            get_player.order = GET_FORM_DATA['order']
            #get_player.seasonNumber = GET_FORM_DATA['seasonNumber']
            #get_player.episodeNumber = GET_FORM_DATA['episodeNumber']
            get_player.language = GET_FORM_DATA['language']
            get_player.visibility = GET_FORM_DATA['visibility']
            get_player.type = GET_FORM_DATA['type']
        #### [MOVIE PLAYER, TV PLAYER] EDIT END 

        #### ACCOUNT EDIT BEGIN 
        if table_name == 'account':
            # get db row 
            get_account = account.query.filter_by(idAccount=id_key).first()
            if not get_account: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # get form datas
            GET_FORM_DATA = {
                'username': request.form['input___username'],
                'password': request.form['input___password'],
                'securityPassword': request.form['input___securityPassword'],
                'emailAddress': request.form['input___emailAddress'],
                'permission': request.form['select2___permission'],
            }

            get_account.username = GET_FORM_DATA['username']
            # password
            if GET_FORM_DATA['password']: 
              get_account.password = hash_str_hash(get_str=GET_FORM_DATA['password'])

            if GET_FORM_DATA['securityPassword']:
              get_account.securityPassword = hash_str_hash(get_str=GET_FORM_DATA['securityPassword'])
            # end password
            get_account.emailAddress = GET_FORM_DATA['emailAddress']
            get_account.permission = GET_FORM_DATA['permission']
        #### ACCOUNT EDIT END 

        #### PROFILE EDIT BEGIN 
        if table_name == 'profile':
            # get db row 
            get_profile = profile.query.filter_by(idProfile=id_key).first()
            if not get_profile: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # check if a file is uploaded
            uploadFile = request.files['uploadFile']
            if uploadFile:
                CustomFormComponent.upload_file(upload_file=uploadFile, save_folder_path=os.path.join(app.root_path, 'storage', 'profile', get_profile.idProfile))
                return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

            # get form datas
            GET_FORM_DATA = {
                'username': request.form['input___username'],
                'password': request.form['input___password'],
                'biography': request.form['input___biography'],
                'imageAvatar': request.form['input___imageAvatar'],
                'imageBackground': request.form['input___imageBackground'],
                'adult': request.form['select2___adult'],
                'permission': request.form['select2___permission'],
                'private': request.form['select2___private'],
            }

            get_profile.username = GET_FORM_DATA['username']
            get_profile.password = GET_FORM_DATA['password']
            get_profile.biography = GET_FORM_DATA['biography']
            get_profile.imageAvatar = GET_FORM_DATA['imageAvatar']
            get_profile.imageBackground = GET_FORM_DATA['imageBackground']
            get_profile.adult = GET_FORM_DATA['adult']
            get_profile.permission = GET_FORM_DATA['permission']
            get_profile.private = GET_FORM_DATA['private']
        #### PROFILE EDIT END 

        #### CAST EDIT BEGIN 
        if table_name == 'cast':
            # get db row 
            get_cast = cast.query.filter_by(idCast=id_key).first()
            if not get_cast: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # check if a file is uploaded
            uploadFile = request.files['uploadFile']
            if uploadFile:
                CustomFormComponent.upload_file(upload_file=uploadFile, save_folder_path=os.path.join(app.root_path, 'storage', 'cast', get_cast.idCast))
                return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

            # get form datas
            GET_FORM_DATA = {
                'name': request.form['input___name'],
                'nameUrl': request.form['input___nameUrl'],
                'biography': request.form['input___biography'],
                'idTmdb': request.form['input___idTmdb'],
                'idImdb': request.form['input___idImdb'],
                'idTwitter': request.form['input___idTwitter'],
                'idInstagram': request.form['input___idInstagram'],
                'imagePoster': request.form['input___imagePoster'],
                'birthPlace': request.form['input___birthPlace'],
                'birthDate': request.form['input___birthDate'],
                'deathDate': request.form['input___deathDate'],
                'gender': request.form['select2___gender'],
                'adult': request.form['select2___adult'],
                'visibility': request.form['select2___visibility'],
            }

            get_cast.name = GET_FORM_DATA['name']
            get_cast.nameUrl = GET_FORM_DATA['nameUrl']
            get_cast.biography = GET_FORM_DATA['biography']
            get_cast.idTmdb = GET_FORM_DATA['idTmdb']
            get_cast.idImdb = GET_FORM_DATA['idImdb']
            get_cast.idTwitter = GET_FORM_DATA['idTwitter']
            get_cast.idInstagram = GET_FORM_DATA['idInstagram']
            get_cast.imagePoster = GET_FORM_DATA['imagePoster']
            get_cast.birthPlace = GET_FORM_DATA['birthPlace']
            get_cast.birthDate = GET_FORM_DATA['birthDate']
            get_cast.deathDate = GET_FORM_DATA['deathDate']
            get_cast.gender = GET_FORM_DATA['gender']
            get_cast.adult = GET_FORM_DATA['adult']
            get_cast.visibility = GET_FORM_DATA['visibility']
        #### CAST EDIT END 

        #### COLLECTION EDIT BEGIN 
        if table_name == 'collection':
            # get db row 
            get_collection = collection.query.filter_by(idCollection=id_key).first()
            if not get_collection: return error(err_msg="item couldn't be found.", ret_url=url_for('adminpanel_v2_home'))

            # check if a file is uploaded
            uploadFile = request.files['uploadFile']
            if uploadFile:
                CustomFormComponent.upload_file(upload_file=uploadFile, save_folder_path=os.path.join(app.root_path, 'storage', 'collection', get_collection.idCollection))
                return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))

            # get form datas
            GET_FORM_DATA = {
                'title': request.form['input___title'],
                'titleUrl': request.form['input___titleUrl'],
                'overview': request.form['input___overview'],
                'imagePoster': request.form['input___imagePoster'],
                'imageBackground': request.form['input___imageBackground'],
                'private': request.form['select2___private'],
                'recommended': request.form['select2___recommended'],
            }

            get_collection.title = GET_FORM_DATA['title']
            get_collection.titleUrl = GET_FORM_DATA['titleUrl']
            get_collection.overview = GET_FORM_DATA['overview']
            get_collection.imagePoster = GET_FORM_DATA['imagePoster']
            get_collection.imageBackground = GET_FORM_DATA['imageBackground']
            get_collection.private = GET_FORM_DATA['private']
            get_collection.recommended = GET_FORM_DATA['recommended']
        #### COLLECTION EDIT END 

        db.session.commit()
        return redirect(url_for('adminpanel_v2_edit') + '?table={}&id={}'.format(table_name, id_key))
        #else: return error(err_msg='unknown table_name')

    return redirect(url_for('adminpanel_v2_home'))

@app.route('/adminpanel/v2/edit')
def adminpanel_v2_edit():
    if not check_admin(): return redirect(url_for('home'))

    RET_URL = url_for('adminpanel_v2_home')

    ARG_TABLE = request.args.get('table', default=None, type=str)
    ARG_ID = request.args.get('id', default='-', type=str)

    if ARG_TABLE:
        # `content` table begin
        if ARG_TABLE == 'content':

            # query begin
            if not ARG_ID == '-':
                get_edit_item = content.query.filter_by(idContent=ARG_ID).first()
                if not get_edit_item:
                    return redirect(RET_URL)
            else:
                return redirect(RET_URL)
            # query end 

            # url args validation begin
            if not request.args.get('table') or not request.args.get('id'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'id': ARG_ID,
                                                                    }, context = {
                                                                        'data': get_edit_item,
                                                                        'countryList': countryList.query.all(),
                                                                        'languageList': languageList.query.all(),
                                                                        'movieGenreList': movieGenreList.query.all(),
                                                                        'tvGenreList': tvGenreList.query.all(),
                                                                    }, and_=and_, contentCountry=contentCountry, contentLanguage=contentLanguage, movieContentGenre=movieContentGenre, tvContentGenre=tvContentGenre, \
                                                                    files = {
                                                                        'data': os.listdir(os.path.join(app.root_path, 'storage', 'content', ARG_ID))
                                                                    })
        # `content` table end 

        # [`tvseasoncontent`, `tvepisodecontent`] tables begin
        if ARG_TABLE == 'tvseasoncontent' or ARG_TABLE == 'tvepisodecontent':

            # query begin
            if not ARG_ID == '-':
                if ARG_TABLE == 'tvseasoncontent':
                    _table = tvSeasonContent
                    _id = _table.idTvSeason
                elif ARG_TABLE == 'tvepisodecontent':
                    _table = tvEpisodeContent
                    _id = _table.idTvEpisode
                get_edit_item = _table.query.filter(_id == ARG_ID).first()
                if not get_edit_item:
                    return redirect(RET_URL)
            else:
                return redirect(RET_URL)
            # query end 

            # url args validation begin
            if not request.args.get('table') or not request.args.get('id'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'id': ARG_ID,
                                                                    }, context = {
                                                                        'data': get_edit_item,
                                                                    }, \
                                                                    files = {
                                                                        'data': os.listdir(os.path.join(app.root_path, 'storage', 'content', get_edit_item.idContent))
                                                                    })
        # [`tvseasoncontent`, `tvepisodecontent`] tables end 

        # [`movieplayer`, `tvplayer`] tables begin
        if ARG_TABLE == 'movieplayer' or ARG_TABLE == 'tvplayer':

            # query begin
            if not ARG_ID == '-':
                if ARG_TABLE == 'movieplayer': _table = moviePlayer
                elif  ARG_TABLE == 'tvplayer': _table = tvPlayer
                get_edit_item = _table.query.filter_by(idPlayer=ARG_ID).first()
                if not get_edit_item:
                    return redirect(RET_URL)
            else:
                return redirect(RET_URL)
            # query end 

            # url args validation begin
            if not request.args.get('table') or not request.args.get('id'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'id': ARG_ID,
                                                                    }, context = {
                                                                        'data': get_edit_item,
                                                                    }, \
                                                                    files = {
                                                                        'data': os.listdir(os.path.join(app.root_path, 'storage', 'content', get_edit_item.idContent))
                                                                    })
        # [`movieplayer`, `tvplayer`] tables end 

        # `account` table begin
        if ARG_TABLE == 'account':

            # query begin
            if not ARG_ID == '-':
                get_edit_item = account.query.filter_by(idAccount=ARG_ID).first()
                if not get_edit_item:
                    return redirect(RET_URL)
            else:
                return redirect(RET_URL)
            # query end 

            # url args validation begin
            if not request.args.get('table') or not request.args.get('id'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'id': ARG_ID,
                                                                    }, context = {
                                                                        'data': get_edit_item,
                                                                    }, \
                                                                    files = {
                                                                        #'data': os.listdir(os.path.join(app.root_path, 'storage', 'content', get_edit_item.idContent))
                                                                    })
        # `account` table end 

        # `profile` table begin
        if ARG_TABLE == 'profile':

            # query begin
            if not ARG_ID == '-':
                get_edit_item = profile.query.filter_by(idProfile=ARG_ID).first()
                if not get_edit_item:
                    return redirect(RET_URL)
            else:
                return redirect(RET_URL)
            # query end 

            # url args validation begin
            if not request.args.get('table') or not request.args.get('id'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'id': ARG_ID,
                                                                    }, context = {
                                                                        'data': get_edit_item,
                                                                    }, \
                                                                    files = {
                                                                        'data': os.listdir(os.path.join(app.root_path, 'storage', 'profile', get_edit_item.idProfile))
                                                                    })
        # `profile` table end 

        # `cast` table begin
        if ARG_TABLE == 'cast':

            # query begin
            if not ARG_ID == '-':
                get_edit_item = cast.query.filter_by(idCast=ARG_ID).first()
                if not get_edit_item:
                    return redirect(RET_URL)
            else:
                return redirect(RET_URL)
            # query end 

            # url args validation begin
            if not request.args.get('table') or not request.args.get('id'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'id': ARG_ID,
                                                                    }, context = {
                                                                        'data': get_edit_item,
                                                                    }, \
                                                                    files = {
                                                                        'data': os.listdir(os.path.join(app.root_path, 'storage', 'cast', get_edit_item.idCast))
                                                                    })
        # `cast` table end 

        # `collection` table begin
        if ARG_TABLE == 'collection':

            # query begin
            if not ARG_ID == '-':
                get_edit_item = collection.query.filter_by(idCollection=ARG_ID).first()
                if not get_edit_item:
                    return redirect(RET_URL)
            else:
                return redirect(RET_URL)
            # query end 

            # url args validation begin
            if not request.args.get('table') or not request.args.get('id'): return redirect(RET_URL)
            # url args validation end 

            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', \
                                                                    _ARG = {
                                                                        'table': ARG_TABLE,
                                                                        'id': ARG_ID,
                                                                    }, context = {
                                                                        'data': get_edit_item,
                                                                    }, \
                                                                    files = {
                                                                        'data': os.listdir(os.path.join(app.root_path, 'storage', 'collection', get_edit_item.idCollection))
                                                                    })
        # `collection` table end 

        # `test` table begin
        if ARG_TABLE == 'test':
            return render_template('adminpanel_v2/edit/index.html', title='Düzenleniyor', edit_item_result='--', \
                                                                    _ARG = {
                                                                        'table': 'test',
                                                                        'id': '-',
                                                                    }) 
        # `test` table end 

        # non-exists table begin
        else: return redirect(RET_URL)
        # non-exists table end 
    else: return redirect(RET_URL) 
