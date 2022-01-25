/*
######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################
*/

/*###########################
###### content->seasons
###########################*/
function mainproc_content_seasons_selectFirstPlayer(content_id, tv_season_id, tv_episode_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('mainproc_content_seasons'),
    data: JSON.stringify({
      'function': 'selectFirstPlayer',
      'idContent': content_id,
      'idTvSeason': tv_season_id,
      'idTvEpisode': tv_episode_id,
    }),
    success: function(response){
      if (response.err_msg){
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.err_msg);
        setTimeout(() => {
          $('.alertMainDiv').hide();
        }, 2500);
      }
      else if (response.succ_msg){
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.succ_msg);
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  }));
};

function mainproc_content_seasons_selectRandomEpisode(content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('mainproc_content_seasons'),
    data: JSON.stringify({
      'function': 'selectRandomEpisode',
      'idContent': content_id,
    }),
    success: function(response){
      if (response.err_msg){
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.err_msg);
        setTimeout(() => {
          $('.alertMainDiv').hide();
        }, 2500);
      }
      else if (response.succ_msg){
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.succ_msg);
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  }));
};
/*###########################
###### end content->seasons
###########################*/

/*
######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################
*/

/*###########################
###### content->season->episodes
###########################*/
function mainproc_content_season_episodes_selectNextEpisode(content_id, tv_season_id, tv_episode_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('mainproc_content_season_episodes'),
    data: JSON.stringify({
      'function': 'selectNextEpisode',
      'idContent': content_id,
      'idTvSeason': tv_season_id,
      'idTvEpisode': tv_episode_id,
    }),
    success: function(response){
      if (response.err_msg){
        alert(response.err_msg);
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.err_msg);
        setTimeout(() => {
          $('.alertMainDiv').hide();
        }, 2500);
      }
      else if (response.succ_msg){
        alert(response.succ_msg);
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.succ_msg);
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  }));
};

function mainproc_content_season_episodes_selectPreviousEpisode(content_id, tv_season_id, tv_episode_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('mainproc_content_season_episodes'),
    data: JSON.stringify({
      'function': 'selectPreviousEpisode',
      'idContent': content_id,
      'idTvSeason': tv_season_id,
      'idTvEpisode': tv_episode_id,
    }),
    success: function(response){
      if (response.err_msg){
        alert(response.err_msg);
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.err_msg);
        setTimeout(() => {
          $('.alertMainDiv').hide();
        }, 2500);
      }
      else if (response.succ_msg){
        alert(response.succ_msg);
        $('.alertMainDiv').show();
        $('.alertMainText').text(response.succ_msg);
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  }));
};
/*###########################
###### end content->season->episodes
###########################*/
