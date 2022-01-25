$(document).ready(() => {
  $('#select2___adult').select2();
  $('#select2___permission').select2();
  $('#select2___private').select2();
  $('#form__img').attr("src", `{{context['data'].imageAvatar|safe}}`);
  $('#form__imgBg').attr("src", `{{context['data'].imageBackground|safe}}`);
  $('#input___username').val(`{{context['data'].username|safe}}`);
  $('#input___password').val(`{{context['data'].password|safe}}`);
  $('#input___biography').val(`{{context['data'].biography|safe}}`);
  $('#input___imageAvatar').val(`{{context['data'].imageAvatar|safe}}`);
  $('#input___imageBackground').val(`{{context['data'].imageBackground|safe}}`);
  // select2
  if (`{{context['data'].adult}}` == 1){
    $('#select2-select2___adult-container').text('Yetişkin Hesabı');
    $('#select2___adult').val('1');
  } if (`{{context['data'].adult}}` == 0){
    $('#select2-select2___adult-container').text('Çocuk Hesabı');
    $('#select2___adult').val('0');
  }

  if (`{{context['data'].permission}}` == 'USER'){
    $('#select2-select2___permission-container').text('Kullanıcı');
    $('#select2___permission').val('USER');
  } else if (`{{context['data'].permission}}` == 'EDITOR'){
    $('#select2-select2___permission-container').text('Editör');
    $('#select2___permission').val('EDITOR');
  } else if (`{{context['data'].permission}}` == 'ADMIN'){
    $('#select2-select2___permission-container').text('Kullanıcı');
    $('#select2___permission').val('ADMIN');
  }

  if (`{{context['data'].private}}` == 0){
    $('#select2-select2___private-container').text('Herkese Açık');
    $('#select2___private').val('0');
  } else if (`{{context['data'].private}}` == 1){
    $('#select2-select2___private-container').text('Gizli');
    $('#select2___private').val('1');
  }
});

function select_image(type, file){
  filePath = `/storage/profile/{{context['data'].idProfile}}/${file}`;
  if (type == 'avatar'){ $('#input___imageAvatar').val(filePath); $('#form__img').attr('src', filePath); }
  if (type == 'background'){ $('#input___imageBackground').val(filePath); $('#form__imgBg').attr('src', filePath); }
  $('.modal__btn--dismiss').click();
};
