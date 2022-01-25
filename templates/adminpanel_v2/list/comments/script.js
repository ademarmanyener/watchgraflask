function updateRecord(idComment){
  get_text = $(`#inputText-${idComment}`).val();
  console.log(` ==> ${get_text}`);
  
  if (get_text){
     adminpanel_v2_function(tableName='comments',
                        functionName='updateRecord',
                        dictionary={
                          'table': `{{_ARG['table']}}`,
                          'idComment': idComment,
                          'text': get_text,
                        });     
  }
};
