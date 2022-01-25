$(document).ready(() => {
  // for insert new
	$('#selectInsertNew_gender').select2({
		placeholder: "Cinsiyet",
		allowClear: true
	});
	$('#selectInsertNew_adult').select2({
		placeholder: "Yetişkin İçerik",
		allowClear: true
	});
});

$('#inputImportFromTmdb_queryName').on('input', () => {
  get_query_name = $('#inputImportFromTmdb_queryName').val();

  if (get_query_name){
     adminpanel_v2_function(tableName='cast', functionName='importFromTmdbQuery', dictionary={'queryName': get_query_name});
  }
});

$('#btnInsertNew_insertNew').on('click', () => {
    get_gender = $('#selectInsertNew_gender').val();
    get_name = $('#inputInsertNew_name').val();
    get_nameUrl = $('#inputInsertNew_nameUrl').val();
    get_biography = $('#inputInsertNew_biography').val();
    get_idTmdb = $('#inputInsertNew_idTmdb').val();
    get_idImdb = $('#inputInsertNew_idImdb').val();
    get_idTwitter = $('#inputInsertNew_idTwitter').val();
    get_idInstagram = $('#inputInsertNew_idInstagram').val();
    get_adult = $('#selectInsertNew_adult').val();
    get_birthPlace = $('#inputInsertNew_birthPlace').val();
    get_birthDate = $('#inputInsertNew_birthDate').val();
    get_deathDate = $('#inputInsertNew_deathDate').val();

    if (get_gender && get_name && get_nameUrl && get_idTmdb && get_idImdb && get_adult){
      adminpanel_v2_function(tableName='cast',
                          functionName='insertNew',
                          dictionary={
                            'gender': get_gender,
                            'name': get_name,
                            'nameUrl': get_nameUrl,
                            'biography': get_biography,
                            'idTmdb': get_idTmdb,
                            'idImdb': get_idImdb,
                            'idTwitter': get_idTwitter,
                            'idInstagram': get_idInstagram,
                            'adult': get_adult,
                            'birthPlace': get_birthPlace,
                            'birthDate': get_birthDate,
                            'deathDate': get_deathDate,
                          });    
    }
});
