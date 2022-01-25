# -*- encoding: utf-8 -*-
from includes import *

@app.route('/collections', methods=['POST', 'GET'])
@app.route('/koleksiyonlar', methods=['POST', 'GET'])
def collection_discover():
  if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

  RET_URL = url_for('collection_discover') + '?query=*&page=1&tag=*'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_TAG = request.args.get('tag', default='*', type=str)
  DEF_LIST_COUNT = 32
  DEF_OFFSET = (ARG_PAGE - 1) * DEF_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL)
  # page validation end

  get_recommendations = collection.query.filter(collection.recommended == 1).all()

  # get query filters begin
  if not ARG_QUERY == '*': _db_query_title = collection.title.like('%{}%'.format(ARG_QUERY))
  else: _db_query_title = collection.title.like('%%')

  # query without genre filtering
  get_results = collection.query.filter(and_(_db_query_title, collection.private == 0, collection.recommended == 0)).order_by(collection.addDate.desc()).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(collection.query.filter(and_(_db_query_title, collection.private == 0)).order_by(collection.addDate.desc()).all()) / DEF_LIST_COUNT)

  if not ARG_TAG == '*':
    _def_tag = collectionTag.title.like('%{}%'.format(ARG_TAG))

    get_results = collection.query.join(collectionTag).filter(and_(_def_tag, collection.private == 0, collection.recommended == 0)).order_by(collection.addDate.desc()).offset(DEF_OFFSET).limit(DEF_LIST_COUNT).all()
    DEF_PAGE_MAX = ceil(len(collection.query.join(collectionTag).filter(and_(_def_tag, collection.private == 0)).order_by(collection.addDate.desc()).all()) / DEF_LIST_COUNT)
  # get query filters end

  return render_template('collection/discover.html', title='Koleksiyonları Keşfet', recommendations_info=get_recommendations, results_info=get_results, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'tag': ARG_TAG,
                                          'list_count': DEF_LIST_COUNT,
                                        })

@app.route('/new-collection', methods=['POST', 'GET'])
@app.route('/yeni-koleksiyon', methods=['POST', 'GET'])
def collection_new():
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    form = NewCollectionForm()

    # FORM BEGIN
    if form.validate_on_submit():
        selected_private = 0
        if request.form.getlist('privatecollection'): selected_private = 1

        SELECTED_TITLE_URL = slugify(form.title.data)
        if collection.query.filter(and_(collection.titleUrl == SELECTED_TITLE_URL)).first() != None: SELECTED_TITLE_URL = SELECTED_TITLE_URL + '_' + str(id_generator(chars=string.ascii_letters, size=12))

        db.session.add(collection(
          idAddProfile = session['PROFILE']['idProfile'],
          idAddAccount = session['ACCOUNT']['idAccount'],
          title = form.title.data,
          titleUrl = SELECTED_TITLE_URL,
          overview = form.overview.data,
          private = selected_private,
          imagePoster = '/static/img/defaults/poster_collection.png',
          imageBackground = '/static/img/defaults/background_collection.png',
          recommended = 0,
          lastEditDate = datetime.now()
        ))
        db.session.commit()
        return redirect(url_for('collection_title', title_url=SELECTED_TITLE_URL))
    # FORM END

    return render_template('collection/new.html', title='Yeni Bir Koleksiyon Oluştur', form=form)

@app.route('/collection/<title_url>')
@app.route('/koleksiyon/<title_url>')
def collection_title(title_url):
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    select_collection = collection.query.filter_by(titleUrl=title_url).first()
    if select_collection == None: return error(err_msg='Böyle bir koleksiyon bulunamadı.', ret_url=url_for('home'))

    if select_collection.private == True:
        if check_profile() == True and session['PROFILE']['idProfile'] == select_collection.idAddProfile and session['ACCOUNT']['idAccount'] == select_collection.idAddAccount: pass
        else: return error(err_msg='Bu koleksiyon gizli.', ret_url=url_for('home'))

    select_collection_items = collectionItem.query.filter_by(idCollection=select_collection.idCollection).order_by(collectionItem.index.desc()).order_by(collectionItem.addDate.desc()).all()
    select_collection_tags = collectionTag.query.filter_by(idCollection=select_collection.idCollection).all()

    return render_template('collection/title.html', title=select_collection.title, \
                                                  collection_info=select_collection, \
                                                  collection_items_info=select_collection_items, \
                                                  collection_tags_info=select_collection_tags)

@app.route('/collection/<title_url>/edit', methods=['POST', 'GET'])
@app.route('/koleksiyon/<title_url>/duzenle', methods=['POST', 'GET'])
def collection_edit(title_url):
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    RET_URL = url_for('home')

    select_collection = collection.query.filter(and_(collection.titleUrl == title_url, collection.idAddProfile == session['PROFILE']['idProfile'], collection.idAddAccount == session['ACCOUNT']['idAccount'])).first()
    if select_collection == None: return error(err_msg='Bu ID ile hesabınıza ilişkili bir koleksiyon bulunamadı.', ret_url=url_for('home'))

    select_collection_items = collectionItem.query.filter_by(idCollection=select_collection.idCollection).all()

    """
    try:
      get_posters_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', select_collection.idCollection, 'poster'))
      get_backgrounds_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', select_collection.idCollection, 'background'))
    except:
      get_posters_list = ''
      get_backgrounds_list = ''
    """

    # form begin
    if request.method == 'POST':
      # check if a file is uploaded
      uploadFile_imagePoster = request.files['form__img-upload']
      uploadFile_imageBackground = request.files['form__imgBg-upload']
      if uploadFile_imagePoster:
        CustomFormComponent.upload_file(upload_file=uploadFile_imagePoster, save_folder_path=os.path.join(app.root_path, 'storage', 'collection', select_collection.idCollection), file_type='poster')
        select_collection.imagePoster = '/storage/collection/{}/poster.jpg'.format(select_collection.idCollection)
      if uploadFile_imageBackground:
        CustomFormComponent.upload_file(upload_file=uploadFile_imageBackground, save_folder_path=os.path.join(app.root_path, 'storage', 'collection', select_collection.idCollection), file_type='background')
        select_collection.imageBackground = '/storage/collection/{}/background.jpg'.format(select_collection.idCollection)

      DEF_NEW_TITLE = request.form['input___title']
      # NEW TITLEURL
      DEF_NEW_TITLE_URL = select_collection.titleUrl
      if request.form['input___title'] != select_collection.title:
        DEF_NEW_TITLE_URL = slugify(request.form['input___title'])
        if collection.query.filter(and_(collection.titleUrl == DEF_NEW_TITLE_URL)).first(): DEF_NEW_TITLE_URL = DEF_NEW_TITLE_URL + '_' + str(id_generator(chars=string.ascii_letters, size=12))
        select_collection.titleUrl = DEF_NEW_TITLE_URL
      # END NEW TITLEURL
      DEF_NEW_OVERVIEW = request.form['input___overview']

      """
      ############### !!! DEPRECATED
      # IMAGE UPLOAD BEGIN
      DEF_NEW_IMAGE_POSTER = select_collection.imagePoster
      DEF_NEW_IMAGE_BACKGROUND = select_collection.imageBackground
      try:
        if request.form.getlist('poster'):
          DEF_NEW_IMAGE_POSTER = '/storage/collection/{}/poster/{}'.format(select_collection.idCollection, request.form.getlist('poster')[0])
        else:
          temp_new_uploaded_poster = request.files['form__img-upload']
          if temp_new_uploaded_poster:
            temp_secure_filename = secure_filename(temp_new_uploaded_poster.filename)
            temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
            temp_new_uploaded_poster.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', select_collection.idCollection, 'poster', temp_generate_filename))
            DEF_NEW_IMAGE_POSTER = '/storage/collection/{}/poster/{}'.format(select_collection.idCollection, temp_generate_filename)
          else:
            DEF_NEW_IMAGE_POSTER = request.form['input___imagePoster']

        if request.form.getlist('background'):
          DEF_NEW_IMAGE_BACKGROUND = '/storage/collection/{}/background/{}'.format(select_collection.idCollection, request.form.getlist('background')[0])
        else:
          temp_new_uploaded_background = request.files['form__imgBg-upload']
          if temp_new_uploaded_background:
            temp_secure_filename = secure_filename(temp_new_uploaded_background.filename)
            temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
            temp_new_uploaded_background.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', select_collection.idCollection, 'background', temp_generate_filename))
            DEF_NEW_IMAGE_BACKGROUND = '/storage/collection/{}/background/{}'.format(select_collection.idCollection, temp_generate_filename)
          else:
            DEF_NEW_IMAGE_BACKGROUND = request.form['input___imageBackground']
      except: pass
      # IMAGE UPLOAD END
      """

      DEF_NEW_PRIVATE = False
      if request.form.getlist('privatecollection'): DEF_NEW_PRIVATE = True

      # variable validation begin
      if len(DEF_NEW_TITLE) >= 4 and len(DEF_NEW_TITLE) <= 35: pass
      else: return error(err_msg='Koleksiyon için geçersiz kullanıcı adı seçildi.', ret_url=RET_URL)
      if collection.query.filter(and_(collection.idCollection != select_collection.idCollection, collection.titleUrl == DEF_NEW_TITLE_URL)).first(): return error(err_msg='Bu url adıyla zaten bir koleksiyon mevcut.', ret_url=RET_URL)
      # variable validation end

      select_collection.title = DEF_NEW_TITLE
      select_collection.titleUrl = DEF_NEW_TITLE_URL
      select_collection.overview = DEF_NEW_OVERVIEW
      #select_collection.imagePoster = '/storage/collection/{}/poster.jpg'.format(select_collection.idCollection)
      #select_collection.imageBackground = '/storage/collection/{}/background.jpg'.format(select_collection.idCollection)
      select_collection.private = DEF_NEW_PRIVATE

      db.session.commit()

      return redirect(url_for('collection_edit', title_url=DEF_NEW_TITLE_URL))
    # form end

    return render_template('collection/edit.html', title='Koleksiyonu Düzenle', \
                                                   context = {
                                                    'data': select_collection,
                                                    'items': select_collection_items,
                                                   })

@app.route('/collection/<collection_id>/delete')
@app.route('/koleksiyon/<collection_id>/sil')
def collection_delete(collection_id):
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    select_collection = collection.query.filter(and_(collection.idCollection == collection_id, collection.idAddProfile == session['PROFILE']['idProfile'], collection.idAddAccount == session['ACCOUNT']['idAccount'])).first()
    if select_collection == None: return error(err_msg='Bu ID ile hesabınıza ilişkili bir koleksiyon bulunamadı.', ret_url=url_for('home'))

    select_collection.drop()

    return redirect(url_for('collection_discover'))
    #return error(err_msg='Koleksiyonunuz başarıyla silindi.', err_code=':)', ret_url=url_for('home'))
