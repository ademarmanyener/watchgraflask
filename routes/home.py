# -*- encoding: utf-8 -*-
from includes import *

# test
@app.route("/_status/check")
def status_check():
    return os.getenv("TALISKER_REVISION_ID", "OK")

@app.route("/favicon.ico")
def favicon():
    return send_file(
        os.path.join(app.root_path, 'static', 'icon', 'favicon-32x32.png'), mimetype="image/vnd.microsoft.icon"
    )

@app.route('/storage/<path:filename>')
def storage(filename):
  return send_from_directory(os.path.join(app.root_path, 'storage'), filename)

@app.route('/', methods=['POST', 'GET'])
def home():
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    highlight_info = highlightContent.query.all()
    latest_all_info = content.query.order_by(content.addDate.desc()).limit(24).all()
    latest_movie_info = content.query.filter_by(type='MOVIE').order_by(content.addDate.desc()).limit(24).all()
    latest_tv_info = content.query.filter_by(type='TV').order_by(content.addDate.desc()).limit(24).all()
    ### it's actually not random yet! so fix it too!
    random_info = content.query.limit(6).all()
    latest_tv_episodes_info = tvEpisodeContent.query.order_by(tvEpisodeContent.addDate.desc()).limit(18).all() # beta

    if check_profile():
      return render_template('home/private.html', title='Anasayfa', content=content, latestWatchedEpisode=latestWatchedEpisode, highlightContent=highlightContent, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent)
    else:
      return render_template('home/public.html', title='', content=content, highlightContent=highlightContent, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent)

@app.route('/beta/everyone', methods=['POST', 'GET'])
def home_beta_everyone():
  return render_template('home/beta_everyone.html', title='', content=content, highlightContent=highlightContent, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent)

@app.route('/beta/user', methods=['POST', 'GET'])
def home_beta_user():
  return render_template('home/beta_user.html', title='', content=content, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent)
