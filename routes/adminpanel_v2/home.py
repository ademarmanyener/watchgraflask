# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/v2')
def adminpanel_v2_redirect():
    return redirect(url_for('adminpanel_v2_home'))

@app.route('/adminpanel/v2/home', methods=['POST', 'GET'])
def adminpanel_v2_home():
    if not check_admin(): return redirect(url_for('home'))

    select_all_movie_contents = content.query.filter_by(type='MOVIE').all()
    select_all_tv_contents = content.query.filter_by(type='TV').all()
    select_all_movie_comments = movieComment.query.all()
    select_all_tv_comments = tvComment.query.all()
    select_all_tv_title_comments = tvTitleComment.query.all()
    select_all_cast_comments = castComment.query.all()
    select_all_profiles = profile.query.all()
    select_all_casts = cast.query.all()
    select_latest_movie_contents = content.query.filter_by(type='MOVIE').order_by(content.addDate.desc()).limit(10).all()
    select_latest_tv_contents = content.query.filter_by(type='TV').order_by(content.addDate.desc()).limit(10).all()
    select_latest_profiles = profile.query.order_by(profile.addDate.desc()).limit(10).all()
    select_latest_casts = cast.query.order_by(cast.addDate.desc()).limit(10).all()

    return render_template('adminpanel_v2/home/index.html', title='', \
                                                        all_movie_contents_info=select_all_movie_contents, \
                                                        all_tv_contents_info=select_all_tv_contents, \
                                                        all_movie_comments_info=select_all_movie_comments, \
                                                        all_tv_comments_info=select_all_tv_comments, \
                                                        all_tv_title_comments_info=select_all_tv_title_comments, \
                                                        all_cast_comments_info=select_all_cast_comments, \
                                                        all_profiles_info=select_all_profiles, \
                                                        all_casts_info=select_all_casts, \
                                                        latest_movie_contents_info=select_latest_movie_contents, \
                                                        latest_tv_contents_info=select_latest_tv_contents, \
                                                        latest_profiles_info=select_latest_profiles, \
                                                        latest_casts_info=select_latest_casts)
