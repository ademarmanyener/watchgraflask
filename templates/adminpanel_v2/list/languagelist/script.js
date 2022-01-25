$('#btnInsertNew_insertNew').on('click', () => {
  get_idISO_639_1 = $('#inputInsertNew_idISO_639_1').val();
  get_title = $('#inputInsertNew_title').val();
  get_titleOriginal = $('#inputInsertNew_titleOriginal').val();

  if (get_idISO_639_1 && get_title && get_titleOriginal){
    adminpanel_v2_function(tableName='languagelist',
                        functionName='insertNew',
                        dictionary={
                          'idISO_639_1': get_idISO_639_1,
                          'title': get_title,
                          'titleOriginal': get_titleOriginal,
                        });    
  }
});

function updateRecord(idISO_639_1){
  get_title = $(`#inputTitle-${idISO_639_1}`).val();
  get_titleOriginal = $(`#inputTitleOriginal-${idISO_639_1}`).val();
  console.log(` ==> ${get_title} - ${get_titleOriginal}`);
  
  if (get_title && get_titleOriginal){
     adminpanel_v2_function(tableName='languagelist',
                        functionName='updateRecord',
                        dictionary={
                          'idISO_639_1': idISO_639_1,
                          'title': get_title,
                          'titleOriginal': get_titleOriginal,
                        });     
  }
};
