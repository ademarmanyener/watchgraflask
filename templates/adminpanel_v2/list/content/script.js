$(document).ready(() => {
  // for import from tmdb
	$('#selectImportFromTmdb_type').select2({
		placeholder: "Film mi dizi mi?",
		allowClear: true
	});

  // for insert new
	$('#selectInsertNew_type').select2({
		placeholder: "Film mi dizi mi?",
		allowClear: true
	});
});

$('#inputImportFromTmdb_queryTitle').on('input', () => {
  get_type = $('#selectImportFromTmdb_type').val();
  get_query_title = $('#inputImportFromTmdb_queryTitle').val();

  if (get_type && get_query_title){
     adminpanel_v2_function(tableName='content', functionName='importFromTmdbQuery', dictionary={'queryTitle': get_query_title, 'type': get_type});
  }
});

$('#selectImportFromTmdb_type').change(() => {
  $('#queryTBody').empty();
});

$('#btnInsertNew_insertNew').on('click', () => {
    get_title = $('#inputInsertNew_title').val();
    get_titleOriginal = $('#inputInsertNew_titleOriginal').val();
    get_titleUrl = $('#inputInsertNew_titleUrl').val();
    get_overview = $('#inputInsertNew_overview').val();
    get_idTmdb = $('#inputInsertNew_idTmdb').val();
    get_idImdb = $('#inputInsertNew_idImdb').val();
    get_type = $('#selectInsertNew_type').val();

    if (get_title && get_titleOriginal && get_titleUrl){
      adminpanel_v2_function(tableName='content',
                          functionName='insertNew',
                          dictionary={
                            'title': get_title,
                            'titleOriginal': get_titleOriginal,
                            'titleUrl': get_titleUrl,
                            'overview': get_overview,
                            'idTmdb': get_idTmdb,
                            'idImdb': get_idImdb,
                            'type': get_type,
                          });    
    }
});

function fetchThePopulars(type){
  if (!type)
    return 1;

  var AVAILABLE_TYPES = ['MOVIE', 'TV'];
  if (!AVAILABLE_TYPES.includes(type))
    return 1;

  adminpanel_v2_function(tableName='content',
                      functionName='fetchThePopulars',
                      dictionary={
                        'type': type,
                      });

  return 0;
};

function fetchTheClassics(type){
  if (!type)
    return 1;

  var AVAILABLE_TYPES = ['MOVIE', 'TV'];
  if (!AVAILABLE_TYPES.includes(type))
    return 1;

  adminpanel_v2_function(tableName='content',
                      functionName='fetchTheClassics',
                      dictionary={
                        'type': type,
                      });

  return 0;
};
