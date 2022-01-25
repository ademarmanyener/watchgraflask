$(document).ready(() => {});

$('#btnInsertNew_insertNew').on('click', () => {
    get_title = $('#inputInsertNew_title').val();
    get_overview = $('#inputInsertNew_overview').val();
    get_idTmdb = $('#inputInsertNew_idTmdb').val();
    get_seasonNumber = $('#inputInsertNew_seasonNumber').val();
    get_airDate = $('#inputInsertNew_airDate').val();

    if (get_title && get_seasonNumber){
      adminpanel_v2_function(tableName='tvseasoncontent',
                          functionName='insertNew',
                          dictionary={
                            'title': get_title,
                            'overview': get_overview,
                            'idTmdb': get_idTmdb,
                            'seasonNumber': get_seasonNumber,
                            'airDate': get_airDate,
                          });    
    }
});
