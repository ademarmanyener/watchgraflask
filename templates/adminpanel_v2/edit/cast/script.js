$(document).ready(() => {
  $('#select2___gender').select2();
  $('#select2___adult').select2();
  $('#select2___visibility').select2();
  $('#form__img').attr("src", `{{context['data'].imagePoster|safe}}`);
  $('#input___name').val(`{{context['data'].name|safe}}`);
  $('#input___nameUrl').val(`{{context['data'].nameUrl|safe}}`);
  $('#input___biography').val(`{{context['data'].biography|safe}}`);
  $('#input___idTmdb').val(`{{context['data'].idTmdb|safe}}`);
  $('#input___idImdb').val(`{{context['data'].idImdb|safe}}`);
  $('#input___idTwitter').val(`{{context['data'].idTwitter|safe}}`);
  $('#input___idInstagram').val(`{{context['data'].idInstagram|safe}}`);
  $('#input___imagePoster').val(`{{context['data'].imagePoster|safe}}`);
  $('#input___birthPlace').val(`{{context['data'].birthPlace|safe}}`);
  $('#input___birthDate').val(`{{context['data'].birthDate|safe}}`);
  $('#input___deathDate').val(`{{context['data'].deathDate|safe}}`);
  // select2
  if (`{{context['data'].gender}}` == '0'){
    $('#select2-select2___gender-container').text('Belirtilmedi');
    $('#select2___gender').val('0');
  } else if (`{{context['data'].gender}}` == '1'){
    $('#select2-select2___gender-container').text('Kadın');
    $('#select2___gender').val('1');
  } else if (`{{context['data'].gender}}` == '2'){
    $('#select2-select2___gender-container').text('Erkek');
    $('#select2___gender').val('2');
  } else if (`{{context['data'].gender}}` == '3'){
    $('#select2-select2___gender-container').text('Non-Binary');
    $('#select2___gender').val('3');
  }

  if (`{{context['data'].adult}}` == 0){
    $('#select2-select2___adult-container').text('Herkese Uygun');
    $('#select2___adult').val('0');
  } if (`{{context['data'].adult}}` == 1){
    $('#select2-select2___adult-container').text('Yetişkin İçerik');
    $('#select2___adult').val('1');
  }

  if (`{{context['data'].visibility}}` == 0){
    $('#select2-select2___visibility-container').text('Gizli');
    $('#select2___visibility').val('0');
  } else if (`{{context['data'].visibility}}` == 1){
    $('#select2-select2___visibility-container').text('Herkese Açık');
    $('#select2___visibility').val('1');
  }

});

function select_image(type, file){
  filePath = `/storage/cast/{{context['data'].idCast}}/${file}`;
  if (type == 'poster'){ $('#input___imagePoster').val(filePath); $('#form__img').attr('src', filePath); }
  $('.modal__btn--dismiss').click();
};
