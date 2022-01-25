/*
if check_admin() == True
then also include that
javascript
*/

/*###########################
###### highlight
###########################*/
function adminproc_highlights_addOrDrop(content_input){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_highlights")}}',
    url: Flask.url_for('adminproc_highlights'),
    data: JSON.stringify({
      'function': 'addOrDrop',
      'inputContent': content_input,
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
        try {
          $(`#main__table--tr-${content_input}`).remove();
          $(`#modal-drop-${content_input} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};
/*###########################
###### end highlight
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
###### contents 
###########################*/
function adminproc_contents_visibilitySwitch(content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_contents")}}',
    url: Flask.url_for('adminproc_contents'),
    data: JSON.stringify({
      'function': 'visibilitySwitch',
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
        window.location.reload();
      }
    },
  })); 
};

function adminproc_contents_drop(content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_contents")}}',
    url: Flask.url_for('adminproc_contents'),
    data: JSON.stringify({
      'function': 'drop',
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
        try {
          $(`#main__table--tr-${content_id}`).remove();
          $(`#modal-drop-${content_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};

function adminproc_contents_tmdbImport(tmdb_id, type){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_contents")}}',
    url: Flask.url_for('adminproc_contents'),
    data: JSON.stringify({
      'function': 'tmdbImport',
      'idTmdb': tmdb_id,
      'type': type,
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
        //window.location.reload();
        try {
          //$(`#modal-contents-addMenu_TV_TMDB .modal__btn--dismiss`).click();
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};

function adminproc_contents_createNatural(type){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_contents")}}',
    url: Flask.url_for('adminproc_contents'),
    data: JSON.stringify({
      'function': 'createNatural',
      'type': type,
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
        //window.location.reload();
        try {
          //$(`#modal-contents-addMenu_TV_TMDB .modal__btn--dismiss`).click();
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};
/*###########################
###### end contents 
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
###### content->players
###########################*/
function adminproc_content_players_drop(player_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_content_players")}}',
    url: Flask.url_for('adminproc_content_players'),
    data: JSON.stringify({
      'function': 'drop',
      'idPlayer': player_id,
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
        try {
          $(`#main__table--tr-${player_id}`).remove();
          $(`#modal-drop-${player_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};

function adminproc_content_players_tmdbImport(tmdb_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_players'),
    data: JSON.stringify({
      'function': 'tmdbImport',
      'idTmdb': tmdb_id,
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};

function adminproc_content_players_createNatural(content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_players'),
    data: JSON.stringify({
      'function': 'createNatural',
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};
/*###########################
###### end content->players
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
###### content->seasons 
###########################*/
function adminproc_content_seasons_drop(season_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_content_seasons")}}',
    url: Flask.url_for('adminproc_content_seasons'),
    data: JSON.stringify({
      'function': 'drop',
      'idTvSeason': season_id,
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
        try {
          $(`#main__table--tr-${season_id}`).remove();
          $(`#modal-drop-${season_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};

function adminproc_content_seasons_tmdbImport(tmdb_id, season_number){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_seasons'),
    data: JSON.stringify({
      'function': 'tmdbImport',
      'idTmdb': tmdb_id,
      'seasonNumber': season_number,
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};

function adminproc_content_seasons_createNatural(content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_seasons'),
    data: JSON.stringify({
      'function': 'createNatural',
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
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
function adminproc_content_season_episodes_drop(episode_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_content_season_episodes")}}',
    url: Flask.url_for('adminproc_content_season_episodes'),
    data: JSON.stringify({
      'function': 'drop',
      'idTvEpisode': episode_id,
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
        try {
          $(`#main__table--tr-${episode_id}`).remove();
          $(`#modal-drop-${episode_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};

function adminproc_content_season_episodes_tmdbImport(tmdb_id, season_number, episode_number){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_season_episodes'),
    data: JSON.stringify({
      'function': 'tmdbImport',
      'idTmdb': tmdb_id,
      'seasonNumber': season_number,
      'episodeNumber': episode_number,
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};

function adminproc_content_season_episodes_createNatural(content_id, tv_season_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_season_episodes'),
    data: JSON.stringify({
      'function': 'createNatural',
      'idContent': content_id,
      'idTvSeason': tv_season_id,
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
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
###### content->season->episode->players 
###########################*/
function adminproc_content_season_episode_players_drop(player_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    //url: '{{url_for("adminproc_content_season_episode_players")}}',
    url: Flask.url_for('adminproc_content_season_episode_players'),
    data: JSON.stringify({
      'function': 'drop',
      'idPlayer': player_id,
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
        try {
          $(`#main__table--tr-${player_id}`).remove();
          $(`#modal-drop-${player_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};

function adminproc_content_season_episode_players_tmdbImport(tmdb_id, season_number, episode_number){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_season_episode_players'),
    data: JSON.stringify({
      'function': 'tmdbImport',
      'idTmdb': tmdb_id,
      'seasonNumber': season_number,
      'episodeNumber': episode_number,
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};

function adminproc_content_season_episode_players_createNatural(content_id, tv_season_id, tv_episode_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_content_season_episode_players'),
    data: JSON.stringify({
      'function': 'createNatural',
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
        try {
          $(`.modal .modal__btn--dismiss`).click();
        } catch(err) {console.log(` ERR => ${err}`);}
      }
      else if (response.ret_url){
        window.location.href = response.ret_url;
      }
    },
  })); 
};
/*###########################
###### end content->season->episode->players 
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
###### accounts 
###########################*/
function adminproc_accounts_drop(account_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_accounts'),
    data: JSON.stringify({
      'function': 'drop',
      'idAccount': account_id,
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
        try {
          $(`#main__table--tr-${account_id}`).remove();
          $(`#modal-drop-${account_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};
/*###########################
###### end accounts 
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
###### profiles 
###########################*/
function adminproc_profiles_drop(profile_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_profiles'),
    data: JSON.stringify({
      'function': 'drop',
      'idProfile': profile_id,
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
        try {
          $(`#main__table--tr-${profile_id}`).remove();
          $(`#modal-drop-${profile_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};
/*###########################
###### end profiles 
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
###### casts 
###########################*/
function adminproc_casts_drop(cast_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_casts'),
    data: JSON.stringify({
      'function': 'drop',
      'idCast': cast_id,
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
        try {
          $(`#main__table--tr-${cast_id}`).remove();
          $(`#modal-drop-${cast_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};
/*###########################
###### end casts 
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
###### collections 
###########################*/
function adminproc_collections_drop(collection_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_collections'),
    data: JSON.stringify({
      'function': 'drop',
      'idCollection': collection_id,
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
        try {
          $(`#main__table--tr-${collection_id}`).remove();
          $(`#modal-drop-${collection_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};
/*###########################
###### end collections 
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
###### comments 
###########################*/
function adminproc_comments_drop(comment_id, type){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminproc_comments'),
    data: JSON.stringify({
      'function': 'drop',
      'idComment': comment_id,
      'type': type,
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
        try {
          $(`#main__table--tr-${comment_id}`).remove();
          $(`#modal-drop-${comment_id} .modal__btn--dismiss`).click();
        }
        catch {}
      }
    },
  })); 
};
/*###########################
###### end comments 
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