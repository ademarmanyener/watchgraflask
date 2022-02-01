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

@app.route('/', methods=['GET'])
def home():
  if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

  # if a profile signed in
  if check_profile():
    query = dict(
      latest_watched_episodes = latestWatchedEpisode.query.filter_by(
        idAddAccount = get_logged_account().idAccount,
        idAddProfile = get_logged_profile().idProfile,
      ).order_by(latestWatchedEpisode.watchDate.desc()).all(),
      latest_added_episodes = tvEpisodeContent.query.filter_by(
        visibility = 1,
      ).order_by(tvEpisodeContent.addDate.desc(), tvEpisodeContent.episodeNumber.desc()).all(),
      latest_added_movies = content.query.filter_by(
        visibility = 1,
        type = 'MOVIE',
      ).order_by(content.addDate.desc()).all(),
    )
    return render_template('home/private.html', title='Anasayfa', context=query)

  # if anonymous 
  else:
    most_watched_series = content.query.filter_by(
      visibility = 1,
      type = 'TV',
    ).order_by(content.visitCount.desc()).limit(5).all()
    most_watched_movies = content.query.filter_by(
      visibility = 1,
      type = 'MOVIE',
    ).order_by(content.visitCount.desc()).limit(5).all()
    most_voted_contents = content.query.filter_by(
      visibility = 1,
    ).order_by(content.voteAverage.desc()).limit(9).all()
    latest_added_contents = content.query.filter_by(
      visibility = 1,
    ).order_by(content.addDate.desc()).limit(125).all()
    latest_added_episodes = tvEpisodeContent.query.filter_by(
      visibility = 1,
    ).order_by(tvEpisodeContent.addDate.desc(), tvEpisodeContent.episodeNumber.desc()).limit(35).all()
    highlighted_contents = highlightContent.query.order_by(highlightContent.highlightDate.desc()).all()

    return render_template('home/public.html', \
                                                      most_watched_series=most_watched_series, \
                                                      most_watched_movies=most_watched_movies, \
                                                      most_voted_contents=most_voted_contents, \
                                                      latest_added_contents=latest_added_contents, \
                                                      latest_added_episodes=latest_added_episodes, \
                                                      highlighted_contents=highlighted_contents)
  return 'this place looks so lonely.'

@app.route('/beta/everyone', methods=['POST', 'GET'])
def home_beta_everyone():
  return render_template('home/beta_everyone.html', title='', content=content, highlightContent=highlightContent, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent)

@app.route('/beta/user', methods=['POST', 'GET'])
def home_beta_user():
  return render_template('home/beta_user.html', title='', content=content, tvSeasonContent=tvSeasonContent, tvEpisodeContent=tvEpisodeContent)
