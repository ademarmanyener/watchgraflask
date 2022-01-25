$(document).ready(() => {
  // for insert new
	$('#selectInsertNew_idAccount').select2({
		placeholder: "Hesap ID'si",
		allowClear: true
	});
	$('#selectInsertNew_adult').select2({
		placeholder: "Yetişkinlik",
		allowClear: true
	});
	$('#selectInsertNew_permission').select2({
		placeholder: "Yetki",
		allowClear: true
	});
	$('#selectInsertNew_private').select2({
		placeholder: "Gizlilik",
		allowClear: true
	});
});

$('#btnInsertNew_insertNew').on('click', () => {
  get_idAccount = $('#inputInsertNew_queryAccount').val();

  get_username = $('#inputInsertNew_username').val();
  get_password = $('#inputInsertNew_password').val();
  get_biography = $('#inputInsertNew_biography').val();

  get_adult = $('#selectInsertNew_adult').val();
  get_permission = $('#selectInsertNew_permission').val();
  get_private = $('#selectInsertNew_private').val();

  if (get_idAccount && get_username && get_adult && get_permission && get_private){
    adminpanel_v2_function(tableName='profile',
                        functionName='insertNew',
                        dictionary={
                          'idAccount': get_idAccount,
                          'username': get_username,
                          'password': get_password,
                          'biography': get_biography,
                          'adult': get_adult,
                          'permission': get_permission,
                          'private': get_private,
                        });    
  }
});

$('#inputInsertNew_queryAccount').on('input', () => {
  get_query_account = $('#inputInsertNew_queryAccount').val();

  if (get_query_account){
     adminpanel_v2_function(tableName='profile', functionName='insertNewQuery', dictionary={'queryAccount': get_query_account});
  }
});
