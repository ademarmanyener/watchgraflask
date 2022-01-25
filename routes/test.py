# -*- encoding: utf-8 -*-
from includes import *

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    im = Image.open(im)
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    new_im = new_im.convert('RGB')
    new_im.save(os.path.join(app.root_path, 'storage', 'test.jpg'), 'JPEG')

@app.route('/test/pillow')
def test_pillow():
    # /storage/content/content_21VripXgBhDdW9cHytgRlfD4j3fDNBctND/JS4Uyx8tfDvlVXuh21.jpg
    image_path1 = '/storage/content/content_21VripXgBhDdW9cHytgRlfD4j3fDNBctND/JS4Uyx8tfDvlVXuh21.jpg'
    image_path2 = '/storage/test.jpg'
    from PIL import Image
    make_square(im=os.path.join(app.root_path, 'storage', 'content', 'content_21VripXgBhDdW9cHytgRlfD4j3fDNBctND', 'JS4Uyx8tfDvlVXuh21.jpg'), min_size=70000)
    return render_template('test/pillow.html', image1=image_path1, image2=image_path2)

@app.route('/test/db_query')
def test_query():
    return render_template('/test/db_query.html', db=db, and_=and_, content=content, movieContentGenre=movieContentGenre,
            _ARG = {
                'canonical_url': '/deneme/dbQuery',
            })

@app.route('/test/macro')
def test_macro(): return render_template('test/macro.html')

@app.route('/test/macro2')
def test_macro2():
    first_content = content.query.first()
    return render_template('test/macro2.html', first_content=first_content)

@app.route('/test/segment')
def test_segment(): return render_template('test/test_segment.html', content=content)

@app.route('/test/jq-live')
def test_jq_live():
    return render_template('test/test_jq_live.html')

@app.route('/test/jq-live/function', methods=['POST'])
def test_jq_live_function():
    if not check_admin(): return make_response(jsonify({'err_msg': 'unvalid permission.'}))
    if not request.is_json: return make_response(jsonify({'err_msg': 'unvalid `JSON`.'}))

    GET_DICTIONARY = request.get_json()['dictionary']

    if GET_DICTIONARY['query']:
        # select_results = content.query.filter(content.title.like('%{}%'.format(GET_DICTIONARY['query']))).order_by(content.title.asc()).all()
        # if select_results:
            # listID = []
            # listPoster = []
            # listTitle = []
            # for rs in select_results:
                # listID.append(rs.idContent)
            # for rs in select_results:
                # listTitle.append(rs.title)
            # for rs in select_results:
                # listPoster.append(rs.imagePoster)
            # return make_response(jsonify({'succ_msg': 'OK.', 'resultsID': listID, 'resultsTitle': listTitle, 'resultsPoster': listPoster}))

            #tmdb.Search().movie(query='Adem')['results'][0]['id']

        select_results = tmdb.Search().tv(query=GET_DICTIONARY['query'], language=TMDB_LANGUAGE)['results']
        if select_results:
            listID = []
            listPoster = []
            listTitle = []
            for rs in select_results:
                listID.append(rs['id'])
            for rs in select_results:
                listTitle.append(rs['name'])
            for rs in select_results:
                listPoster.append('https://www.themoviedb.org/t/p/w600_and_h900_bestv2' + str(rs['poster_path']))
            return make_response(jsonify({'succ_msg': 'OK.', 'resultsID': listID, 'resultsTitle': listTitle, 'resultsPoster': listPoster}))
        else:
            return make_response(jsonify({'err_msg': 'NOPE.'}))

@app.route('/test/fetch_popular')
def test_fetch_popular():
    #if not check_admin(): return redirect(url_for('home'))

    get_popular = tmdb.Movies().popular(language=TMDB_LANGUAGE, page=1)['results']

    for p in get_popular:
        if content.query.filter(and_(content.type == 'MOVIE', content.idTmdb == str(p['id']))).first():
            print('exists {}'.format(p['title']))
        else: print('doesnt exist {}'.format(p['title']))

    return str(get_popular)
