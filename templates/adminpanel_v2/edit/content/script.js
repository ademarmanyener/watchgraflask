$(document).ready(() => {
  $('#select2___adult').select2();
  $('#select2___visibility').select2();
  $('#select2___type').select2();
  $('#select2___country').select2({'placeholder': 'Ülke'});
  $('#select2___language').select2({'placeholder': 'Dil'});
  $('#select2___genre').select2({'placeholder': 'Tür'});
  $('#form__img').attr("src", `{{context['data'].imagePoster|safe}}`);
  $('#form__imgBg').attr("src", `{{context['data'].imageBackground|safe}}`);
  $('#input___title').val(`{{context['data'].title|safe}}`);
  $('#input___titleOriginal').val(`{{context['data'].titleOriginal|safe}}`);
  $('#input___titleUrl').val(`{{context['data'].titleUrl|safe}}`);
  $('#input___overview').val(`{{context['data'].overview|safe}}`);
  $('#input___voteAverage').val(`{{context['data'].voteAverage|safe}}`);
  $('#input___idTmdb').val(`{{context['data'].idTmdb|safe}}`);
  $('#input___idImdb').val(`{{context['data'].idImdb|safe}}`);
  $('#input___imagePoster').val(`{{context['data'].imagePoster|safe}}`);
  $('#input___imageBackground').val(`{{context['data'].imageBackground|safe}}`);
  $('#input___releaseDate').val(`{{context['data'].releaseDate|safe}}`);
  // select2
  if (`{{context['data'].adult}}` == 0){
    $('#select2-select2___adult-container').text('Herkese Açık');
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

  if (`{{context['data'].type}}` == 'MOVIE'){
    $('#select2-select2___type-container').text('Film');
    $('#select2___type').val('MOVIE');
  } else if (`{{context['data'].type}}` == 'TV'){
    $('#select2-select2___type-container').text('Dizi');
    $('#select2___type').val('TV');
  }
});

function select_image(type, file){
  filePath = `/storage/content/{{context['data'].idContent}}/${file}`;
  if (type == 'poster'){ $('#input___imagePoster').val(filePath); $('#form__img').attr('src', filePath); }
  if (type == 'background'){ $('#input___imageBackground').val(filePath); $('#form__imgBg').attr('src', filePath); }
  $('.modal__btn--dismiss').click();
};
