# -*- encoding: utf-8 -*-
from includes import *

"""
ajax codes for all kind of profiles
"""

###########################
###### home
###########################
@app.route('/profileproc/home/latestEpisodes/loadMore', methods=['POST'])
def profileproc_home_latestEpisodes_loadMore():
    if not check_profile(): return make_response(jsonify({'err_msg': 'Giriş yapmamışsınız!'}))

    if request.is_json == False: return error(err_msg='JSON değil.')
    load_count = request.get_json()['loadCount']
    cards_length = request.get_json()['cardsLength']
    load_offset = request.get_json()['loadOffset']

    select_episodes = tvEpisodeContent.query.order_by(tvEpisodeContent.addDate.desc()).limit(load_count).offset(load_offset).all()

    list_imagePoster = []
    list_title = []
    list_titleUrl = []
    list_seasonNumber = []
    list_episodeNumber = []
    list_voteAverage = []
    for result in select_episodes:
        list_imagePoster.append(result.imagePoster)
        list_title.append(content.query.filter_by(idContent=result.idContent).first().title) 
        list_titleUrl.append(content.query.filter_by(idContent=result.idContent).first().titleUrl) 
        list_seasonNumber.append(result.seasonNumber)
        list_episodeNumber.append(result.episodeNumber)
        list_voteAverage.append(result.voteAverage)

    return make_response(jsonify({'succ_msg': 'Daha fazla içerik yüklendi.', \
                                    'list_imagePoster': list_imagePoster, \
                                    'list_title': list_title, \
                                    'list_titleUrl': list_titleUrl, \
                                    'list_seasonNumber': list_seasonNumber, \
                                    'list_episodeNumber': list_episodeNumber, \
                                    'list_voteAverage': list_voteAverage, \
                                    }))
###########################
###### end home
###########################

###########################
###### collection
###########################
@app.route('/profileproc/collection/addcontent', methods=['POST'])
def profileproc_collection_addcontent():
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    if request.is_json == False: return error(err_msg='JSON değil.')
    collection_id = request.get_json()['idCollection']
    content_id = request.get_json()['idContent']

    select_collection = collection.query.filter(and_(collection.idCollection == collection_id, collection.idAddProfile == session['PROFILE']['idProfile'], collection.idAddAccount == session['ACCOUNT']['idAccount'])).first()
    if select_collection == None: return make_response(jsonify({'err_msg': 'Bu ID ile hesabınıza ilişkili bir koleksiyon bulunamadı.'}))

    select_content = content.query.filter_by(idContent=content_id).first()
    if select_content == None: return make_response(jsonify({'err_msg': 'Bu ID ile ilişkili bir içerik bulunamadı.'}))

    select_collection_item = collectionItem.query.filter(and_(collectionItem.idCollection == collection_id, collectionItem.idContent == content_id)).first()
    if select_collection_item != None: return make_response(jsonify({'err_msg': 'Bu içeriği seçilen koleksiyona zaten eklemişsiniz.'}))

    db.session.add(collectionItem(
      idCollection = collection_id,
      idAddProfile = session['PROFILE']['idProfile'],
      idAddAccount = session['ACCOUNT']['idAccount'],
      idContent = content_id
    ))
    db.session.commit()

    return make_response(jsonify({'succ_msg': 'Bu içerik başarıyla koleksiyonunuza eklendi.'}))

@app.route('/profileproc/collection/dropcontent', methods=['POST'])
def profileproc_collection_dropcontent():
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    if request.is_json == False: return error(err_msg='JSON değil.')
    collection_id = request.get_json()['idCollection']
    content_id = request.get_json()['idContent']

    select_collection = collection.query.filter(and_(collection.idCollection == collection_id, collection.idAddProfile == session['PROFILE']['idProfile'], collection.idAddAccount == session['ACCOUNT']['idAccount'])).first()
    if select_collection == None: return make_response(jsonify({'err_msg': 'Bu ID ile hesabınıza ilişkili bir koleksiyon bulunamadı.'}))

    select_content = content.query.filter_by(idContent=content_id).first()
    if select_content == None: return make_response(jsonify({'err_msg': 'Bu ID ile ilişkili bir içerik bulunamadı.'}))

    select_collection_item = collectionItem.query.filter(and_(collectionItem.idCollection == collection_id, collectionItem.idContent == content_id)).first()
    if select_collection_item == None: return make_response(jsonify({'err_msg': 'Bu içerik, seçilen koleksiyonda zaten mevcut değil.'}))

    select_collection_item.drop()

    return make_response(jsonify({'succ_msg': 'Bu içerik başarıyla koleksiyonunuzdan kaldırıldı.'}))
###########################
###### end collection
###########################

###########################
###### tvepisodecontent
###########################
@app.route('/profileproc/tvepisodecontent/clearlatestwatchedepisodes', methods=['POST'])
def profileproc_tvepisodecontent_clearlatestwatchedepisodes():
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    if request.is_json == False: return error(err_msg='JSON değil.')

    select_latest_watched_episodes = latestWatchedEpisode.query.filter_by(idAddProfile=session['PROFILE']['idProfile']).all()
    for latest_watched_episode in select_latest_watched_episodes:
        latest_watched_episode.drop()

    return make_response(jsonify({'succ_msg': 'Son izlenilen bölümler temizlendi.'}))

@app.route('/profileproc/tvepisodecontent/addtolatestwatchedepisode', methods=['POST'])
def profileproc_tvepisodecontent_addtolatestwatchedepisode():
    if not check_profile(): return make_response(jsonify({'ret_url': url_for('home')}))

    if not request.is_json: return error(err_msg='JSON değil.')

    content_id = request.get_json()['idContent']
    tv_season_id = request.get_json()['idTvSeason']
    tv_episode_id = request.get_json()['idTvEpisode']

    # check if episode exists
    if not tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == content_id, tvEpisodeContent.idTvSeason == tv_season_id, tvEpisodeContent.idTvEpisode == tv_episode_id)).first(): return make_response(jsonify({'err_msg': 'Bu ID ile ilişkili bir bölüm bulunamadı.'}))

    # check if this user already has this episode watched, if not then add
    if latestWatchedEpisode.query.filter(and_(latestWatchedEpisode.idAddProfile == session['PROFILE']['idProfile'], latestWatchedEpisode.idTvEpisode == tv_episode_id)).first(): pass
    else:
        db.session.add(latestWatchedEpisode(
            idContent = content_id,
            idTvSeason = tv_season_id,
            idTvEpisode = tv_episode_id,
            idAddProfile = session['PROFILE']['idProfile'],
            idAddAccount = session['ACCOUNT']['idAccount'],
        ))
        db.session.commit()
        return make_response(jsonify({'succ_msg': 'Bu bölüm, son izlenilenlere eklendi.'}))
###########################
###### end tvepisodecontent
###########################
