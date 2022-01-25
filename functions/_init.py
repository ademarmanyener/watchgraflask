# -*- encoding: utf-8 -*-
from includes import *
from termcolor import colored

#🔘
#😂
#😫
#✔️
#❗
#❌

# INIT FUNCTION -- BETA
@app.route('/_init/fetch_tmdb')
def init_fetch_tmdb():
    if check_admin():
        if request.args.get('page'):
            if request.args.get('page') == 'popular':
                _fetch_from = {
                        'movie': tmdb.Movies().popular,
                        'tv': tmdb.TV().popular,
                }
            if request.args.get('page') == 'top_rated':
                _fetch_from = {
                        'movie': tmdb.Movies().top_rated,
                        'tv': tmdb.TV().top_rated,
                }
        else: return redirect(url_for('home'))
        _TIME_SLEEP = 2
        if request.args.get('page_begin'): __page_begin = int(request.args.get('page_begin'))
        else: __page_begin = 1
        if request.args.get('page_end'): __page_end = int(request.args.get('page_end'))
        else: __page_begin = 2
        _PAGE = {
                "start": __page_begin,
                "end": __page_end,

        }
        for _page in range(_PAGE['start'], _PAGE['end']):
            for _result in _fetch_from['movie'](page=_page)['results']:
                print(colored(" [movie]", attrs=['bold']), 'Checking for', colored('{}'.format(_result['title']), attrs=['bold']) + '...')
                if not content.query.filter(and_(content.idTmdb == _result['id'], content.type == 'MOVIE')).first():
                    print(colored(' [...]', 'yellow', attrs=['bold', 'blink']), 'Adding', colored('{}.'.format(_result['title']), attrs=['bold']))
                    try:
                        TMDBSimpleasy.Movie.addComprehensive(get_tmdb_id=_result['id'])
                        print(colored(' [✓]', 'green', attrs=['bold']), colored('{}'.format(_result['title']), attrs=['bold']), 'is added.')
                    except Exception as e:
                        print(colored(' [𐄂]', 'red', attrs=['bold']), colored('An error occured.', attrs=['bold']))
                    time.sleep(_TIME_SLEEP)
                else:
                    print(colored(' [⚠]', 'blue', attrs=['bold']), colored('{}'.format(_result['title']), attrs=['bold']), 'exists so it is passed.')
                print()

        for _page in range(_PAGE['start'], _PAGE['end']):
            for _result in _fetch_from['tv'](page=_page)['results']:
                print(colored(" [tv]", attrs=['bold']), 'Checking for', colored('{}'.format(_result['name']), attrs=['bold']) + '...')
                if not content.query.filter(and_(content.idTmdb == _result['id'], content.type == 'TV')).first():
                    print(colored(' [...]', 'yellow', attrs=['bold', 'blink']), 'Adding', colored('{}.'.format(_result['name']), attrs=['bold']))
                    try:
                        TMDBSimpleasy.TV.addComprehensive(get_tmdb_id=_result['id'])
                        print(colored(' [✓]', 'green', attrs=['bold']), colored('{}'.format(_result['name']), attrs=['bold']), 'is added.')
                    except Exception as e:
                        print(colored(' [𐄂]', 'red', attrs=['bold']), colored('An error occured.', attrs=['bold']))
                    time.sleep(_TIME_SLEEP)
                else:
                    print(colored(' [⚠]', 'blue', attrs=['bold']), colored('{}'.format(_result['name']), attrs=['bold']), 'exists so it is passed.')
                print()

    return 'OK. page: {}, page_begin: {}, page_end: {}'.format(request.args.get('page'), __page_begin, __page_end)

@app.route('/_init/login', methods=['POST', 'GET'])
def init_login():
    ENTERABLE = True 
    if not ENTERABLE: return redirect(url_for('home'))

    LOGIN_PASS = '123456789' # Feel free to change that.

    if request.method == 'POST':
        if LOGIN_PASS == request.form['input_loginPass']:
            run_init()
            return 'OK! return to <a href={}>home</a>'.format(url_for('home'))
        else:
            return 'Wrong Password! return back to <a href={}>login page</a>'.format(url_for('init_login'))

    return render_template('_init/login.html', context = {'failedLoginAttempts': 0}) # BETA, not working

def run_init():
    #### FOLDER
    profile_dir = os.path.join(STORAGE_PATH, 'profile')
    cast_dir = os.path.join(STORAGE_PATH, 'cast')
    collection_dir = os.path.join(STORAGE_PATH, 'collection')
    content_dir = os.path.join(STORAGE_PATH, 'content')

    # mkdir: /storage/profile/
    if not os.path.exists(profile_dir): os.makedirs(profile_dir)

    # mkdir: /storage/cast/
    if not os.path.exists(cast_dir): os.makedirs(cast_dir)

    # mkdir: /storage/collection/
    if not os.path.exists(collection_dir): os.makedirs(collection_dir)

    # mkdir: /storage/content/
    if not os.path.exists(content_dir): os.makedirs(content_dir)
    #### END FOLDER

    for gmg in tmdb.Genres().movie_list(language='en')['genres']:
        if movieGenreList.query.filter_by(idGenre=str(gmg['id'])).first() == None: db.session.add(movieGenreList(gmg['id'], gmg['name'], gmg['name']))

    for gmg in tmdb.Genres().tv_list(language='en')['genres']:
        if tvGenreList.query.filter_by(idGenre=str(gmg['id'])).first() == None: db.session.add(tvGenreList(gmg['id'], gmg['name'], gmg['name']))

    for gl in tmdb.Configuration().languages(language='en'):
        if languageList.query.filter_by(idISO_639_1=gl['iso_639_1']).first() == None: db.session.add(languageList(gl['iso_639_1'], gl['english_name'], gl['english_name']))

    for gc in tmdb.Configuration().countries(language='en'):
        if countryList.query.filter_by(idISO_3166_1=gc['iso_3166_1']).first() == None: db.session.add(countryList(gc['iso_3166_1'], gc['english_name'], gc['english_name']))

    ##### CREATE 'DOCKER' ACCOUNT & PROFILE
    ## the reason we're creating this account & profile
    ## is, when some user removes his/her profile or account
    ## we're planning to transfer from those accounts/profiles
    ## to that docker account/profile
    ###################################
    DOCKER_ACCOUNT_USERNAME = 'WGRAF_SYS'
    DOCKER_PROFILE_USERNAME = 'DOCKER'
    if account.query.filter_by(username=DOCKER_ACCOUNT_USERNAME).first() == None:
        db.session.add(account(
            username = DOCKER_ACCOUNT_USERNAME,
            password = hash_str_hash(get_str='doesnt really matter'),
            securityPassword = hash_str_hash(get_str='doesnt really matter'),
            emailAddress = '-',
            permission = 'SYSTEM', # THAT'S THE MOST IMPORTANT FIELD HERE
            lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
        ))
        if profile.query.filter_by(username=DOCKER_PROFILE_USERNAME).first() == None:
            db.session.add(profile(
                idAccount = account.query.filter_by(username=DOCKER_ACCOUNT_USERNAME).first().idAccount,
                username = DOCKER_PROFILE_USERNAME,
                password = '',
                biography = '',
                adult = True,
                permission = 'DOCKER', # THAT'S THE SECOND MOST IMPORTANT FIELD HERE
                private = True,
                imageAvatar = '/static/img/default_image_avatar.png',
                imageBackground = '/static/img/default_image_background.jpg',
                lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
            ))

    db.session.commit()
    return 0
