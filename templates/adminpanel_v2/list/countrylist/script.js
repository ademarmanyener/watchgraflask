$('#btnInsertNew_insertNew').on('click', () => {
  get_idISO_3166_1 = $('#inputInsertNew_idISO_3166_1').val();
  get_title = $('#inputInsertNew_title').val();
  get_titleOriginal = $('#inputInsertNew_titleOriginal').val();

  if (get_idISO_3166_1 && get_title && get_titleOriginal){
    adminpanel_v2_function(tableName='countrylist',
                        functionName='insertNew',
                        dictionary={
                          'idISO_3166_1': get_idISO_3166_1,
                          'title': get_title,
                          'titleOriginal': get_titleOriginal,
                        });    
  }
});

function updateRecord(idISO_3166_1){
  get_title = $(`#inputTitle-${idISO_3166_1}`).val();
  get_titleOriginal = $(`#inputTitleOriginal-${idISO_3166_1}`).val();
  console.log(` ==> ${get_title} - ${get_titleOriginal}`);
  
  if (get_title && get_titleOriginal){
     adminpanel_v2_function(tableName='countrylist',
                        functionName='updateRecord',
                        dictionary={
                          'idISO_3166_1': idISO_3166_1,
                          'title': get_title,
                          'titleOriginal': get_titleOriginal,
                        });     
  }
};
