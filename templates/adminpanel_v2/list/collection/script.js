$(document).ready(() => {
  // for insert new
	$('#selectInsertNew_idAddProfile').select2({
		placeholder: "Ekleyen Profil ID'si",
		allowClear: true
	});
	$('#selectInsertNew_private').select2({
		placeholder: "Gizlilik",
		allowClear: true
	});
	$('#selectInsertNew_recommended').select2({
		placeholder: "Öne Çıkarılma Durumu",
		allowClear: true
	});
});

$('#btnInsertNew_insertNew').on('click', () => {
    get_idAddProfile = $('#inputInsertNew_queryProfile').val();
    get_title = $('#inputInsertNew_title').val();
    get_titleUrl = $('#inputInsertNew_titleUrl').val();
    get_overview = $('#inputInsertNew_overview').val();
    get_private = $('#selectInsertNew_private').val();
    get_recommended = $('#selectInsertNew_recommended').val();

    if (get_idAddProfile && get_title && get_titleUrl && get_private && get_recommended){
      adminpanel_v2_function(tableName='collection',
                          functionName='insertNew',
                          dictionary={
                            'idAddProfile': get_idAddProfile,
                            'title': get_title,
                            'titleUrl': get_titleUrl,
                            'overview': get_overview,
                            'private': get_private,
                            'recommended': get_recommended,
                          });    
    }
});

$('#inputInsertNew_queryProfile').on('input', () => {
  get_query_profile = $('#inputInsertNew_queryProfile').val();

  if (get_query_profile){
     adminpanel_v2_function(tableName='collection', functionName='insertNewQuery', dictionary={'queryProfile': get_query_profile});
  }
});
