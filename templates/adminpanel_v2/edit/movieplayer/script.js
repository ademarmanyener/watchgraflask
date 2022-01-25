$(document).ready(() => {
  $('#select2___language').select2();
  $('#select2___visibility').select2();
  $('#select2___type').select2();
  $('#form__img').attr("src", `{{url_for('static', filename='img/defaults/poster_player.png')|safe}}`);
  $('#input___title').val(`{{context['data'].title|safe}}`);
  $('#input___viewKey').val(`{{context['data'].viewKey|safe}}`);
  $('#input___source').val(`{{context['data'].source|safe}}`);
  $('#input___order').val(`{{context['data'].order|safe}}`);
  $('#input___imagePoster').val(`{{context['data'].imagePoster|safe}}`);
  // select2
  if (`{{context['data'].language}}` == 'ORIGINAL'){
    $('#select2-select2___language-container').text('Orjinal Dil');
    $('#select2___language').val('ORIGINAL');
  } else if (`{{context['data'].language}}` == 'SUBBED'){
    $('#select2-select2___language-container').text('Altyazı');
    $('#select2___language').val('SUBBED');
  } else if (`{{context['data'].language}}` == 'DUBBED'){
    $('#select2-select2___language-container').text('Dublaj');
    $('#select2___language').val('DUBBED');
  }

  if (`{{context['data'].visibility}}` == 0){
    $('#select2-select2___visibility-container').text('Gizli');
    $('#select2___visibility').val('0');
  } else if (`{{context['data'].visibility}}` == 1){
    $('#select2-select2___visibility-container').text('Herkese Açık');
    $('#select2___visibility').val('1');
  }

  if (`{{context['data'].type}}` == 'IFRAME'){
    $('#select2-select2___type-container').text('iFrame');
    $('#select2___type').val('IFRAME');
  } else if (`{{context['data'].type}}` == 'VIDEOJS'){
    $('#select2-select2___type-container').text('VideoJS');
    $('#select2___type').val('VIDEOJS');
  } else if (`{{context['data'].type}}` == 'PLYR'){
    $('#select2-select2___type-container').text('PLYR');
    $('#select2___type').val('PLYR');
  } else if (`{{context['data'].type}}` == 'TRAILER'){
    $('#select2-select2___type-container').text('Fragman');
    $('#select2___type').val('TRAILER');
  }
});

function select_image(type, file){
  filePath = `/storage/content/{{context['data'].idContent}}/${file}`;
  if (type == 'player'){ $('#input___source').val(filePath); $('#form__img').attr('src', filePath); }
  $('.modal__btn--dismiss').click();
};
