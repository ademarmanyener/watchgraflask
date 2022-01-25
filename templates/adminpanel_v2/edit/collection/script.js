$(document).ready(() => {
  $('#select2___private').select2();
  $('#select2___recommended').select2();
  $('#form__img').attr("src", `{{context['data'].imagePoster|safe}}`);
  $('#form__imgBg').attr("src", `{{context['data'].imageBackground|safe}}`);
  $('#input___title').val(`{{context['data'].title|safe}}`);
  $('#input___titleUrl').val(`{{context['data'].titleUrl|safe}}`);
  $('#input___overview').val(`{{context['data'].overview|safe}}`);
  $('#input___imagePoster').val(`{{context['data'].imagePoster|safe}}`);
  $('#input___imageBackground').val(`{{context['data'].imageBackground|safe}}`);
  // select2
  if (`{{context['data'].private}}` == 0){
    $('#select2-select2___private-container').text('Herkese Açık');
    $('#select2___private').val('0');
  } if (`{{context['data'].private}}` == 1){
    $('#select2-select2___private-container').text('Gizli');
    $('#select2___private').val('1');
  }

  if (`{{context['data'].recommended}}` == 0){
    $('#select2-select2___recommended-container').text('Öne Çıkarılmamış');
    $('#select2___recommended').val('0');
  } else if (`{{context['data'].recommended}}` == 1){
    $('#select2-select2___recommended-container').text('Öne Çıkarılmış');
    $('#select2___recommended').val('1');
  }

});

function select_image(type, file){
  filePath = `/storage/collection/{{context['data'].idCollection}}/${file}`;
  if (type == 'poster'){ $('#input___imagePoster').val(filePath); $('#form__img').attr('src', filePath); }
  if (type == 'background'){ $('#input___imageBackground').val(filePath); $('#form__imgBg').attr('src', filePath); }
  $('.modal__btn--dismiss').click();
};
