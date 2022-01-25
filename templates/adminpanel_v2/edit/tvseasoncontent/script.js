$(document).ready(() => {
  $('#select2___visibility').select2();
  $('#form__img').attr("src", `{{context['data'].imagePoster|safe}}`);
  $('#input___title').val(`{{context['data'].title|safe}}`);
  $('#input___overview').val(`{{context['data'].overview|safe}}`);
  $('#input___idTmdb').val(`{{context['data'].idTmdb|safe}}`);
  $('#input___imagePoster').val(`{{context['data'].imagePoster|safe}}`);
  $('#input___seasonNumber').val(`{{context['data'].seasonNumber|safe}}`);
  $('#input___airDate').val(`{{context['data'].airDate|safe}}`);
  // select2
  if (`{{context['data'].visibility}}` == 0){
    $('#select2-select2___visibility-container').text('Gizli');
    $('#select2___visibility').val('0');
  } else if (`{{context['data'].visibility}}` == 1){
    $('#select2-select2___visibility-container').text('Herkese Açık');
    $('#select2___visibility').val('1');
  }
});

function select_image(type, file){
  filePath = `/storage/content/{{context['data'].idContent}}/${file}`;
  if (type == 'poster'){ $('#input___imagePoster').val(filePath); $('#form__img').attr('src', filePath); }
  $('.modal__btn--dismiss').click();
};
