$(document).ready(() => {
  $('#select2___permission').select2();
  $('#input___username').val(`{{context['data'].username|safe}}`);
  $('#input___password').attr('placeholder', `{{context['data'].password|safe}}`);
  $('#input___securityPassword').attr('placeholder', `{{context['data'].securityPassword|safe}}`);
  $('#input___emailAddress').val(`{{context['data'].emailAddress|safe}}`);
  // select2
  if (`{{context['data'].permission}}` == 'USER'){
    $('#select2-select2___permission-container').text('Kullanıcı');
    $('#select2___permission').val('USER');
  } if (`{{context['data'].permission}}` == 'SYSTEM'){
    $('#select2-select2___permission-container').text('Sistem');
    $('#select2___permission').val('SYSTEM');
  }
});
