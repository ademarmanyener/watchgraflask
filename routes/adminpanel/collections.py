# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/collections')
@app.route('/yoneticipaneli/koleksiyonlar')
def adminpanel_collections():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_collections') + '?query=*&page=1&sort=newest&list_count=10'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_SORT = request.args.get('sort', default='newest', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if not ARG_QUERY == '*':
    _db_query_id = collection.idCollection.like('%{}%'.format(ARG_QUERY))
    _db_query_title = collection.title.like('%{}%'.format(ARG_QUERY))
    _db_query_title_url = collection.titleUrl.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_id = collection.idCollection.like('%%')
    _db_query_title = collection.title.like('%%')
    _db_query_title_url = collection.titleUrl.like('%%')

  if ARG_SORT == 'a-to-z': _db_sort = collection.title.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = collection.title.desc() 
  if ARG_SORT == 'newest': _db_sort = collection.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = collection.addDate.asc()
  # get query filters end

  get_collections = collection.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_url)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(collection.query.filter(or_(_db_query_id, _db_query_title, _db_query_title_url)).all()) / ARG_LIST_COUNT)

  # url args validation begin
  if not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/collections/list.html', title='Tüm Koleksiyonlar', collections_info=get_collections, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/collection/<title_url>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/koleksiyon/<title_url>/duzenle', methods=['POST', 'GET'])
def adminpanel_collection_edit(title_url):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_collection = collection.query.filter(collection.titleUrl == title_url).first()
  if not get_collection: return redirect(RET_URL)

  try:
    get_posters_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', get_collection.idCollection, 'poster'))
    get_backgrounds_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', get_collection.idCollection, 'background'))
  except:
    get_posters_list = ''
    get_backgrounds_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_TITLE = request.form['input___title']
    DEF_NEW_TITLE_URL = request.form['input___titleUrl']
    DEF_NEW_OVERVIEW = request.form['input___overview']

    # IMAGE UPLOAD BEGIN
    DEF_NEW_IMAGE_POSTER = get_collection.imagePoster
    DEF_NEW_IMAGE_BACKGROUND = get_collection.imageBackground
    try:
      if request.form.getlist('poster'):
        DEF_NEW_IMAGE_POSTER = '/storage/collection/{}/poster/{}'.format(get_collection.idCollection, request.form.getlist('poster')[0])
      else:
        temp_new_uploaded_poster = request.files['form__img-upload']
        if temp_new_uploaded_poster:
          temp_secure_filename = secure_filename(temp_new_uploaded_poster.filename)
          temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
          temp_new_uploaded_poster.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', get_collection.idCollection, 'poster', temp_generate_filename))
          DEF_NEW_IMAGE_POSTER = '/storage/collection/{}/poster/{}'.format(get_collection.idCollection, temp_generate_filename)
        else:
          DEF_NEW_IMAGE_POSTER = request.form['input___imagePoster']

      if request.form.getlist('background'):
        DEF_NEW_IMAGE_BACKGROUND = '/storage/collection/{}/background/{}'.format(get_collection.idCollection, request.form.getlist('background')[0])
      else:
        temp_new_uploaded_background = request.files['form__imgBg-upload']
        if temp_new_uploaded_background:
          temp_secure_filename = secure_filename(temp_new_uploaded_background.filename)
          temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
          temp_new_uploaded_background.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'collection', get_collection.idCollection, 'background', temp_generate_filename))
          DEF_NEW_IMAGE_BACKGROUND = '/storage/collection/{}/background/{}'.format(get_collection.idCollection, temp_generate_filename)
        else:
          DEF_NEW_IMAGE_BACKGROUND = request.form['input___imageBackground']
    except: pass
    # IMAGE UPLOAD END 

    DEF_NEW_PRIVATE = int(request.form['select2___private'])
    DEF_NEW_RECOMMENDED = int(request.form['select2___recommended'])

    # variable validation begin
    if collection.query.filter(and_(collection.idCollection != get_collection.idCollection, collection.titleUrl == DEF_NEW_TITLE_URL)).first(): return error(err_msg='Bu url adıyla zaten bir koleksiyon mevcut.', ret_url=RET_URL)
    # variable validation end 

    get_collection.title = DEF_NEW_TITLE
    get_collection.titleUrl = DEF_NEW_TITLE_URL
    get_collection.overview = DEF_NEW_OVERVIEW
    get_collection.imagePoster = DEF_NEW_IMAGE_POSTER
    get_collection.imageBackground = DEF_NEW_IMAGE_BACKGROUND
    get_collection.private = DEF_NEW_PRIVATE
    get_collection.recommended = DEF_NEW_RECOMMENDED

    db.session.commit()

    return redirect(url_for('adminpanel_collection_edit', title_url=DEF_NEW_TITLE_URL))
  # form end

  return render_template('adminpanel/collections/edit.html', title='Düzenleniyor: {}'.format(get_collection.title), collection_info=get_collection, posters_list_info=get_posters_list, backgrounds_list_info=get_backgrounds_list)
