# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/casts')
@app.route('/yoneticipaneli/oyuncular')
def adminpanel_casts():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_casts') + '?query=*&page=1&gender=*&sort=newest&list_count=10'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_GENDER = request.args.get('gender', default='*', type=str)
  ARG_SORT = request.args.get('sort', default='newest', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if not ARG_QUERY == '*':
    _db_query_id = cast.idCast.like('%{}%'.format(ARG_QUERY))
    _db_query_name = cast.name.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_id = cast.idCast.like('%%')
    _db_query_name = cast.name.like('%%')

  if ARG_SORT == 'a-to-z': _db_sort = cast.name.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = cast.name.desc() 
  if ARG_SORT == 'newest': _db_sort = cast.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = cast.addDate.asc()

  _db_gender = cast.gender.like('%%')
  if not ARG_GENDER == '*':
    if ARG_GENDER == 'female': _db_gender = cast.gender == 1
    elif ARG_GENDER == 'male': _db_gender = cast.gender == 2
    else: _db_gender = cast.gender.like('%%')
  # get query filters end

  get_casts = cast.query.filter(and_(or_(_db_query_id, _db_query_name), _db_gender)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(cast.query.filter(and_(or_(_db_query_id, _db_query_name), _db_gender)).all()) / ARG_LIST_COUNT)

  # url args validation begin
  if not request.args.get('page') or not request.args.get('gender') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/casts/list.html', title='Tüm Oyuncular', casts_info=get_casts, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'gender': ARG_GENDER,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/cast/<name_url>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/oyuncu/<name_url>/duzenle', methods=['POST', 'GET'])
def adminpanel_cast_edit(name_url):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_cast = cast.query.filter(cast.nameUrl == name_url).first()
  if not get_cast: return redirect(RET_URL)

  try:
    get_posters_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'cast', get_cast.idCast, 'poster'))
  except:
    get_posters_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_NAME = request.form['input___name']
    DEF_NEW_NAME_URL = request.form['input___nameUrl']
    DEF_NEW_BIOGRAPHY = request.form['input___biography']

    # IMAGE UPLOAD BEGIN
    DEF_NEW_IMAGE_POSTER = get_cast.imagePoster
    try:
      if request.form.getlist('poster'):
        DEF_NEW_IMAGE_POSTER = '/storage/cast/{}/poster/{}'.format(get_cast.idCast, request.form.getlist('poster')[0])
      else:
        temp_new_uploaded_poster = request.files['form__img-upload']
        if temp_new_uploaded_poster:
          temp_secure_filename = secure_filename(temp_new_uploaded_poster.filename)
          temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
          temp_new_uploaded_poster.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'cast', get_cast.idCast, 'poster', temp_generate_filename))
          DEF_NEW_IMAGE_POSTER = '/storage/cast/{}/poster/{}'.format(get_cast.idCast, temp_generate_filename)
        else:
          DEF_NEW_IMAGE_POSTER = request.form['input___imagePoster']
    except: pass
    # IMAGE UPLOAD END 

    DEF_NEW_ID_TMDB = request.form['input___idTmdb']
    DEF_NEW_ID_IMDB = request.form['input___idImdb']
    DEF_NEW_ID_TWITTER = request.form['input___idTwitter']
    DEF_NEW_ID_INSTAGRAM = request.form['input___idInstagram']

    DEF_NEW_BIRTH_PLACE = request.form['input___birthPlace']
    DEF_NEW_BIRTH_DATE = request.form['input___birthDate']
    DEF_NEW_DEATH_DATE = request.form['input___deathDate']

    DEF_NEW_GENDER = int(request.form['select2___gender'])
    DEF_NEW_ADULT = int(request.form['select2___adult'])
    DEF_NEW_VISIBILITY = int(request.form['select2___visibility'])

    # variable validation begin
    if cast.query.filter(and_(cast.idCast != get_cast.idCast, cast.nameUrl == DEF_NEW_NAME_URL)).first(): return error(err_msg='Bu url adıyla zaten bir oyuncu mevcut.', ret_url=RET_URL)
    # variable validation end 

    get_cast.name = DEF_NEW_NAME
    get_cast.nameUrl = DEF_NEW_NAME_URL
    get_cast.biography = DEF_NEW_BIOGRAPHY
    get_cast.imagePoster = DEF_NEW_IMAGE_POSTER
    get_cast.idTmdb = DEF_NEW_ID_TMDB
    get_cast.idImdb = DEF_NEW_ID_IMDB
    get_cast.idTwitter = DEF_NEW_ID_TWITTER
    get_cast.idInstagram = DEF_NEW_ID_INSTAGRAM
    get_cast.birthPlace = DEF_NEW_BIRTH_PLACE
    get_cast.birthDate = DEF_NEW_BIRTH_DATE
    get_cast.deathDate = DEF_NEW_DEATH_DATE
    get_cast.gender = DEF_NEW_GENDER
    get_cast.adult = DEF_NEW_ADULT
    get_cast.visibility = DEF_NEW_VISIBILITY

    db.session.commit()

    return redirect(url_for('adminpanel_cast_edit', name_url=DEF_NEW_NAME_URL))
  # form end

  return render_template('adminpanel/casts/edit.html', title='Düzenleniyor: {}'.format(get_cast.name), cast_info=get_cast, posters_list_info=get_posters_list)
