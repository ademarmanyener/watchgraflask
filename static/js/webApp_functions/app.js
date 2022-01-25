var getUrlParameter = function getUrlParameter(sParam) {
  var sPageURL = window.location.search.substring(1),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i;

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=');

    if (sParameterName[0] === sParam) {
      return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
    }
  }
  return false;
};

$('#header_search_button').click(() => {
  _get_query = $('#header_search_input').val();
  if (_get_query){
    _get_ret_url = `${Flask.url_for('search')}?query=${_get_query}&page=1&type=*&sort=a-to-z`
    window.location.href = _get_ret_url;
  } else { console.log('Sorguyu boş bıraktınız.'); }
});

$('#header_search_input').keypress(function(e){
  if (e.which == 13){
    window.location.href = `${Flask.url_for('search')}?query=${$('#header_search_input').val()}&page=1&type=*&sort=a-to-z`;
  }
});

$('#alertMainDiv').on('click', function(){$('.alertMainDiv').hide();});

class alertMainClass {
  show(dictionary={}){
    // get values
    let mainDiv = $('#alertMainDiv');
    let mainText = $('#alertMainText');
    let mainIcon = $('#alertMainIcon');
    // dictionary
    let def_iconClass = 'icon ion-ios-warning';
    let def_text = '';
    let def_backgroundColour = 'linear-gradient(90deg, #95FF7E 0%, #51CC85 100%';
    let def_delay = 2500;
    let def_fadeIn = 200;
    let def_fadeOut = 200;
    if (dictionary['iconClass']){ def_iconClass = dictionary['iconClass']; }
    if (dictionary['text']){ def_text = dictionary['text']; }
    if (dictionary['backgroundColour']){ def_backgroundColour = dictionary['backgroundColour']; }
    if (dictionary['delay']){ def_delay = dictionary['delay']; }
    if (dictionary['fadeIn']){ def_fadeIn = dictionary['fadeIn']; }
    if (dictionary['fadeOut']){ def_fadeOut = dictionary['fadeOut']; }

    // backgroundColour
    mainDiv.css({'background-image': def_backgroundColour});
    // text
    mainText.text(def_text);
    // icon
    //mainIcon.toggleClass('ion-ios-warning ion-ios-trash');
    mainIcon.removeClass();
    mainIcon.addClass(def_iconClass);
    // finally, fade in and out 
    mainDiv.fadeIn(def_fadeIn).delay(def_delay).fadeOut(def_fadeOut);

    console.log(` ==> 1: ${def_iconClass}, 2: ${def_text}, 3: ${def_backgroundColour}`);
  };

  success(dictionary={}){
    let def_iconClass = 'icon ion-ios-checkmark';
    let def_text = dictionary['text'];
    let def_backgroundColour = 'linear-gradient(90deg, #95FF7E 0%, #51CC85 100%)';
    this.show({'text': dictionary['text'], 'iconClass': def_iconClass, 'backgroundColour': def_backgroundColour});
  };

  warning(dictionary={}){
    let def_iconClass = 'icon ion-ios-warning';
    let def_text = dictionary['text'];
    let def_backgroundColour = 'linear-gradient(90deg, #FFF77E 0%, #BDCC51 100%)';
    this.show({'text': dictionary['text'], 'iconClass': def_iconClass, 'backgroundColour': def_backgroundColour});
  };

  error(dictionary={}){
    let def_iconClass = 'icon ion-ios-close';
    let def_text = dictionary['text'];
    let def_backgroundColour = 'linear-gradient(90deg, #FF7E7E 0%, #CC5151 100%)';
    this.show({'text': dictionary['text'], 'iconClass': def_iconClass, 'backgroundColour': def_backgroundColour});
  };
};
let alertMain = new alertMainClass();

function mildReloadPage(){
  Cookies.set('latest-scroll-top', $(window).scrollTop());
  document.location.reload(true);
};
$(document).ready(() => {
  $(window).scrollTop(0);
  /*
  latestScrollTop = Cookies.get('latest-scroll-top');
  if (latestScrollTop){
    $(window).scrollTop(latestScrollTop);
  }
  */
});

function makeHeaderTransparent(){
  alert('DONE');
  $('.header').css('position', 'absolute');
  $('.header').css('background-color', 'transparent');
  $('.header__wrap').css('background-color', 'transparent');
  $('.header__nav').css('background-color', 'transparent');
  $('.header__search').css('background-color', 'transparent');
  $('.header__search').css('box-shadow', '0px 0px');
  $('.header__search').css('border-top', 'unset');
  $('.header__search-content input').css('background-color', 'transparent');
};
