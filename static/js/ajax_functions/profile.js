/*
if check_profile() == True
then also include that
javascript
*/

/*###########################
###### home
###########################*/
$('#button-latestEpisodes-loadMore').on('click', () => {
  let def_loadCount = 30;
  let def_cardsLength = $('.card-latestEpisode').length;
  let def_loadOffset = def_cardsLength + def_loadCount;

  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('profileproc_home_latestEpisodes_loadMore'),
    data: JSON.stringify({
      'loadCount': def_loadCount,
      'cardsLength': def_cardsLength,
      'loadOffset': def_loadOffset,
    }),
    success: function(response){
      if (response.err_msg){
        alertMain.error({'text': response.err_msg});
      }
      else if (response.succ_msg){
        for (let i=0; i<response.list_titleUrl.length; i++){
          $('#button-latestEpisodes-loadMore').before(`

            <!-- card -->
            <div class="col-6 col-sm-4 col-lg-3 col-xl-2 card-latestEpisode">
              <div class="card">
                <div class="card__cover">
                  <img src="${response.list_imagePoster[i]}" alt="">
                  <a href="${Flask.url_for('tv_watch', {'title_url': response.list_titleUrl[i], 'season_number': response.list_seasonNumber[i], 'episode_number': response.list_episodeNumber[i],})}" class="card__play">
                    <i class="icon ion-ios-play"></i>
                  </a>
                </div>
                <div class="card__content">
                  <h3 class="card__title"><a href="${Flask.url_for('tv_title', {'title_url': response.list_titleUrl[i]})}">${response.list_title[i]}</a></h3>
                  <span class="card__rate" style="font-size: 14px;">${response.list_seasonNumber[i]}. Sezon ${response.list_episodeNumber[i]}. Bölüm</span>
                  <span class="card__category"></span>
                  <span class="card__rate"><i class="icon ion-ios-star"></i>${response.list_voteAverage[i]}</span>
                </div>
              </div>
            </div>
            <!-- end card -->

          `); 
        }
        console.log(response.list_title);
      }
    },
  }));
});

function profileproc_home_(home_id, content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('profileproc_home_addcontent'),
    data: JSON.stringify({
      'idCollection': home_id,
      'idContent': content_id,
    }),
    success: function(response){
      if (response.err_msg){
        alertMain.error({'text': response.err_msg});
      }
      else if (response.succ_msg){
        try {
          $('#item_content_' + content_id).remove();
        } catch(e){
          console.log(e);
        }
        alertMain.success({'text': response.succ_msg});
      }
    },
  }));
};
/*###########################
###### end home
###########################*/















/*###########################
###### collection
###########################*/
function profileproc_collection_addcontent(collection_id, content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('profileproc_collection_addcontent'),
    data: JSON.stringify({
      'idCollection': collection_id,
      'idContent': content_id,
    }),
    success: function(response){
      if (response.err_msg){
        alertMain.error({'text': response.err_msg});
      }
      else if (response.succ_msg){
        try {
          $('#item_content_' + content_id).remove();
        } catch(e){
          console.log(e);
        }
        alertMain.success({'text': response.succ_msg});
      }
    },
  }));
};

function profileproc_collection_dropcontent(collection_id, content_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('profileproc_collection_dropcontent'),
    data: JSON.stringify({
      'idCollection': collection_id,
      'idContent': content_id,
    }),
    success: function(response){
      if (response.err_msg){
        alertMain.error({'text': response.err_msg});
      }
      else if (response.succ_msg){
        try {
          $('#item_content_' + content_id).remove();
        } catch(e){
          console.log(e);
        }
        alertMain.success({'text': response.succ_msg});
      }
    },
  }));
};
/*###########################
###### end collection
###########################*/

/*###########################
###### tvepisodecontent
###########################*/
function profileproc_tvepisodecontent_clearLatestWatchedEpisodes(){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('profileproc_tvepisodecontent_clearlatestwatchedepisodes'),
    data: JSON.stringify({
    }),
    success: function(response){
      if (response.err_msg){
        alertMain.error({'text': response.err_msg});
      }
      else if (response.succ_msg){
        window.location.reload();
      }
    },
  }));
};

function profileproc_tvepisodecontent_addToLatestWatchedEpisode(content_id, tv_season_id, tv_episode_id){
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('profileproc_tvepisodecontent_addtolatestwatchedepisode'),
    data: JSON.stringify({
      'idContent': content_id,
      'idTvSeason': tv_season_id,
      'idTvEpisode': tv_episode_id,
    }),
    success: function(response){
      if (response.err_msg){
        alertMain.error({'text': response.err_msg});
      }
      else if (response.succ_msg){
        alertMain.success({'text': response.succ_msg});
      }
    },
  }));
};
/*###########################
###### end tvepisodecontent
###########################*/
