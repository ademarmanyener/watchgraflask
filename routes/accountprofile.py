# -*- encoding: utf-8 -*-
from includes import *

@app.route('/profile/new', methods=['POST', 'GET'])
@app.route('/profil/yeni', methods=['POST', 'GET'])
def accountprofile_new():
    if check_account() == False: return redirect(url_for('home'))

    MAX_PROFILE_COUNT = 9

    select_account = account.query.filter(and_(account.idAccount == get_logged_account().idAccount)).first()
    if select_account == None: return error(err_msg='Böyle bir hesap bulunamadı.', ret_url=url_for('home'))

    select_profiles = profile.query.filter(and_(profile.idAccount == select_account.idAccount)).all()
    if len(select_profiles) >= MAX_PROFILE_COUNT: return error(err_msg='Maksimum profil sayısına ulaştınız.', ret_url=url_for('whoiswatching'))

    form = NewProfileForm()

    # FORM BEGIN
    if form.validate_on_submit():
        if check_username(form.username.data) == False: return error(err_msg='Geçersiz bir kullanıcı adı şeçtiniz.', ret_url=url_for('accountprofile_new'))

        # REMOVE THIS PART
        selected_avatar = random.choice(g.AVATARS_LIST)
        if request.form.getlist('avatar'): selected_avatar = str(request.form.getlist('avatar')[0])

        selected_background = random.choice(g.BACKGROUNDS_LIST)
        if request.form.getlist('background'): selected_background = str(request.form.getlist('background')[0])

        selected_adult = 1
        if request.form.getlist('childaccount'): selected_adult = 0

        # check if a profile in that account exists with this username
        check_profile = profile.query.filter(and_(profile.username == form.username.data, profile.idAccount == get_logged_account().idAccount)).first()
        if check_profile == None:
            db.session.add(profile(
                idAccount = get_logged_account().idAccount,
                username = form.username.data,
                password = form.password.data,
                biography = '',
                adult = selected_adult,
                permission = 'USER',
                private = 0,
                imageAvatar = '/static/img/avatars/' + selected_avatar,
                imageBackground = '/static/img/backgrounds/' + selected_background,
                lastEditDate = datetime.now()
            ))
            db.session.commit()
            return redirect(url_for('whoiswatching'))
        else: return error(err_msg='Bu kullanıcı adıyla zaten bir profiliniz mevcut.', ret_url=url_for('accountprofile_new'))
    # FORM END

    return render_template('accountprofile/new.html', title='Yeni Bir Profil Oluştur', header=False, footer=False, form=form)

@app.route('/<account_username>/profile/<profile_username>', methods=['POST', 'GET'])
@app.route('/<account_username>/profil/<profile_username>', methods=['POST', 'GET'])
def accountprofile(account_username, profile_username):
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    # only admins should be able to enter in
    #if not check_admin(): return redirect(url_for('home'))

    # check account
    get_account = account.query.filter_by(username=account_username).first()
    if get_account == None: return error(err_msg='Böyle bir hesap bulunamadı', ret_url=url_for('home'))

    # check system account
    if get_account.permission == 'SYSTEM': return redirect(url_for('home'))

    # check profile
    get_profile = profile.query.filter(and_(profile.username == profile_username, profile.idAccount == get_account.idAccount)).first()
    if get_profile == None: return error(err_msg='Böyle bir profil bulunamadı.', ret_url=url_for('home'))

    # check privacy
    if get_profile.private == True:
        if check_profile() == True:
            if get_account.idAccount == get_logged_account().idAccount and \
                get_profile.idProfile == current_user.idProfile: pass
        else: return error(err_msg='Bu profil gizli.', ret_url=url_for('home'))

    get_collections = collection.query.filter(and_(collection.idAddProfile == get_profile.idProfile, collection.idAddAccount == get_account.idAccount, collection.private == False)).all()

    get_latest_watched_episode = latestWatchedEpisode.query.filter_by(idAddProfile=get_profile.idProfile).order_by(latestWatchedEpisode.watchDate.desc()).all()

    return render_template('accountprofile/title.html', title="%s'in Profili" % get_profile.username, account_info=get_account, profile_info=get_profile, \
                                                        follower_info=follow.query.filter_by(idFollowingProfile=get_profile.idProfile).order_by(follow.followDate.desc()).all(), following_info=follow.query.filter_by(idFollowerProfile=get_profile.idProfile).order_by(follow.followDate.desc()).all(), \
                                                        collections_info=get_collections, \
                                                        latest_watched_episode_info=get_latest_watched_episode, \
                                                        tvEpisodeContent=tvEpisodeContent, content=content, tvSeasonContent=tvSeasonContent) # BETA BETA BETA BETA - JUST TESTING

@app.route('/<account_username>/profiles', methods=['POST', 'GET'])
@app.route('/<account_username>/profiller', methods=['POST', 'GET'])
def accountprofiles(account_username):
    ret_url = url_for('home')
    if request.args.get('ret_url'): ret_url = request.args.get('ret_url')

    if check_account() == False: return error(err_msg='Profilleri görmek için giriş yapmanız gerek.', ret_url=ret_url)
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_account = account.query.filter_by(username=account_username).first()
    if get_account == None: return error(err_msg='Böyle bir hesap bulunamadı.', ret_url=url_for('home'))

    if get_account.idAccount == get_logged_account().idAccount: pass
    else: return error(err_msg='Bu senin hesabın mı?')

    profiles_info = profile.query.filter_by(idAccount=get_account.idAccount).all()

    return render_template('accountprofile/profiles.html', title="%s'in Profiller" % get_account.username, account_info=get_account, profiles_info=profiles_info)
