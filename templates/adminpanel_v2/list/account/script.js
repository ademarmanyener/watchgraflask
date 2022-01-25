$('#btnInsertNew_insertNew').on('click', () => {
  get_username = $('#inputInsertNew_username').val();
  get_emailAddress = $('#inputInsertNew_emailAddress').val();
  get_password = $('#inputInsertNew_password').val();
  get_securityPassword = $('#inputInsertNew_securityPassword').val();

  if (get_username && get_emailAddress && get_password && get_securityPassword){
    adminpanel_v2_function(tableName='account',
                        functionName='insertNew',
                        dictionary={
                          'username': get_username,
                          'emailAddress': get_emailAddress,
                          'password': get_password,
                          'securityPassword': get_securityPassword,
                        });    
  }
});
