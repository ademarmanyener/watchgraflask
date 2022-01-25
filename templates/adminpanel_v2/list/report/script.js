function updateRecord(idReport){
  get_name = $(`#inputName-${idReport}`).val();
  get_emailAddress = $(`#inputEmailAddress-${idReport}`).val();
  get_title = $(`#inputTitle-${idReport}`).val();
  get_message = $(`#inputMessage-${idReport}`).val();

  console.log(` ==> ${get_title} - ${get_message}`);
  
  if (get_name && get_emailAddress && get_title && get_message){
     adminpanel_v2_function(tableName='report',
                        functionName='updateRecord',
                        dictionary={
                          'idReport': idReport,
                          'name': get_name,
                          'emailAddress': get_emailAddress,
                          'title': get_title,
                          'message': get_message,
                        });     
  }
};
