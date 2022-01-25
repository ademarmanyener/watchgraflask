$('#btnInsertNew_insertNew').on('click', () => {
  get_idGenre = $('#inputInsertNew_idGenre').val();
  get_title = $('#inputInsertNew_title').val();
  get_titleOriginal = $('#inputInsertNew_titleOriginal').val();

  if (get_idGenre && get_title && get_titleOriginal){
    adminpanel_v2_function(tableName='moviegenrelist',
                        functionName='insertNew',
                        dictionary={
                          'idGenre': get_idGenre,
                          'title': get_title,
                          'titleOriginal': get_titleOriginal,
                        });    
  }
});

function updateRecord(idGenre){
  get_title = $(`#inputTitle-${idGenre}`).val();
  get_titleOriginal = $(`#inputTitleOriginal-${idGenre}`).val();
  console.log(` ==> ${get_title} - ${get_titleOriginal}`);
  
  if (get_title && get_titleOriginal){
     adminpanel_v2_function(tableName='moviegenrelist',
                        functionName='updateRecord',
                        dictionary={
                          'idGenre': idGenre,
                          'title': get_title,
                          'titleOriginal': get_titleOriginal,
                        });     
  }
};
