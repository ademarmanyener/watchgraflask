$(document).ready(() => {
  // insert new select2
  $('#selectInsertNew_language').select2();
  $('#selectInsertNew_type').select2();
});

$('#btnInsertNew_insertNew').on('click', () => {
    get_title = $('#inputInsertNew_title').val();
    get_source = $('#inputInsertNew_source').val();
    get_order = $('#inputInsertNew_order').val();
    get_seasonNumber = $('#inputInsertNew_seasonNumber').val();
    get_episodeNumber = $('#inputInsertNew_episodeNumber').val();
    get_language = $('#selectInsertNew_language').val();
    get_type = $('#selectInsertNew_type').val();

    if (get_title && get_source && get_order && get_seasonNumber && get_episodeNumber && get_language && get_type){
      adminpanel_v2_function(tableName='tvplayer',
                          functionName='insertNew',
                          dictionary={
                            'title': get_title,
                            'source': get_source,
                            'order': get_order,
                            'seasonNumber': get_seasonNumber,
                            'episodeNumber': get_episodeNumber,
                            'language': get_language,
                            'type': get_type,
                            '_ARG': {
                              'idContent': `{{_ARG['idContent']}}`,
                              'idTvSeason': `{{_ARG['idTvSeason']}}`,
                              'idTvEpisode': `{{_ARG['idTvEpisode']}}`,
                            },
                          });    
    }
});
