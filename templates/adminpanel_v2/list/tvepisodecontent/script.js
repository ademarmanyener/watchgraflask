$(document).ready(() => {});

$('#btnInsertNew_insertNew').on('click', () => {
    get_title = $('#inputInsertNew_title').val();
    get_overview = $('#inputInsertNew_overview').val();
    get_idTmdb = $('#inputInsertNew_idTmdb').val();
    get_idImdb = $('#inputInsertNew_idImdb').val();
    get_seasonNumber = $('#inputInsertNew_seasonNumber').val();
    get_episodeNumber = $('#inputInsertNew_episodeNumber').val();
    get_airDate = $('#inputInsertNew_airDate').val();

    if (get_title && get_seasonNumber && get_episodeNumber){
      adminpanel_v2_function(tableName='tvepisodecontent',
                          functionName='insertNew',
                          dictionary={
                            'title': get_title,
                            'overview': get_overview,
                            'idTmdb': get_idTmdb,
                            'idImdb': get_idImdb,
                            'seasonNumber': get_seasonNumber,
                            'episodeNumber': get_episodeNumber,
                            'airDate': get_airDate,
                          });    
    }
});
