/*
 * ajax script for adminpanel_v2 // BETA
*/

function adminpanel_v2_function(tableName, functionName, dictionary={}){
  if (tableName == 'content'){
    if (functionName == 'drop'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();     
      $('#gifLoading').show();
    }
    if (functionName == 'importFromTmdb'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();
      $('#gifLoading').show();
    }
    if (functionName == 'fetchThePopulars'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();
      $('#gifLoading').show();
    }
    if (functionName == 'fetchTheClassics'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();
      $('#gifLoading').show();
    }
  }
  if (tableName == 'tvseasoncontent'){
    if (functionName == 'drop'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();     
      $('#gifLoading').show();
    }
    if (functionName == 'importFromTmdb'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();
      $('#gifLoading').show();
    }
  }
  if (tableName == 'tvepisodecontent'){
    if (functionName == 'drop'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();     
      $('#gifLoading').show();
    }
    if (functionName == 'importFromTmdb'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();
      $('#gifLoading').show();
    }
  }
  if (tableName == 'cast'){
    if (functionName == 'drop'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();     
      $('#gifLoading').show();
    }
    if (functionName == 'importFromTmdb'){
      alertMain.warning({'text': 'It can take a while.'});
      $(`.modal .modal__btn--dismiss`).click();
      $('#gifLoading').show();
    }
  }
  $.ajax($.extend(true, DEF_AJAX_CONFIG, {
    url: Flask.url_for('adminpanel_v2_function', {'table_name': tableName, 'function_name': functionName}),
    data: JSON.stringify({
      'dictionary': dictionary,
    }),
    success: function(response){
      if (response.succ_msg){
        if (tableName == 'content'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idContent']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'importFromTmdb'){
            window.location.reload();
          }
          if (functionName == 'importFromTmdbQuery'){
            $('#queryTBody').empty();
            for (let i=0; i<response.list_idTmdb.length; i++){
              $('#queryTBody').append(`
                <tr onclick="adminpanel_v2_function(tableName='content', functionName='importFromTmdb', dictionary={'idTmdb': '${response.list_idTmdb[i]}','type': '${$('#selectImportFromTmdb_type').val()}'})">
                  <td>
                    <div class="main__user" style="margin-bottom: 10px;">
                      <div class="main__avatar" style="min-width: 75px; height: 100px; border-radius: 5px; -webkit-border-radius: 5px;">
                        <div style="width: 100%; height: 100%; background-image: url('${response.list_imagePoster[i]}'); background-size: cover; background-position: center;"></div>
                      </div>
                      <div class="main__meta">
                        <h3>${response.list_title[i]}</h3>
                      </div>
                    </div>
                  </td>
                </tr>
              `);
            }
            console.log(response.list_idTmdb); 
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
          if (functionName == 'fetchThePopulars'){
            window.location.reload();
          }
          if (functionName == 'fetchTheClassics'){
            window.location.reload();
          }
        }
        if (tableName == 'tvseasoncontent'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idTvSeason']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'importFromTmdb'){
            window.location.reload();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
        }
        if (tableName == 'tvepisodecontent'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idTvEpisode']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'importFromTmdb'){
            window.location.reload();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
        }
        if (tableName == 'tvplayer'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idPlayer']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
        }
        if (tableName == 'movieplayer'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idPlayer']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
        }
        if (tableName == 'account'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idAccount']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
        }
        if (tableName == 'profile'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idProfile']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
          if (functionName == 'insertNewQuery'){
            $('#queryTBody').empty();
            for (let i=0; i<response.list_idAccount.length; i++){
              $('#queryTBody').append(`
                <tr onclick="$('#inputInsertNew_queryAccount').val('${response.list_idAccount[i]}');">
                  <td>
                    <div class="main__table-text" style="margin-left: 10px; margin-bottom: 10px;">${response.list_username[i]}</div>
                  </td>
                  <td>
                    <div class="main__table-text" style="margin-left: 10px; margin-bottom: 10px;">${response.list_permission[i]}</div>
                  </td>
                </tr>
              `);
            }
            console.log(response.list_idTmdb); 
          }
        }
        if (tableName == 'cast'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idCast']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'importFromTmdb'){
            window.location.reload();
          }
          if (functionName == 'importFromTmdbQuery'){
            $('#queryTBody').empty();
            for (let i=0; i<response.list_idTmdb.length; i++){
              $('#queryTBody').append(`
                <tr onclick="adminpanel_v2_function(tableName='cast', functionName='importFromTmdb', dictionary={'idTmdb': '${response.list_idTmdb[i]}'})">
                  <td>
                    <div class="main__user" style="margin-bottom: 10px;">
                      <div class="main__avatar" style="min-width: 75px; height: 125px; border-radius: 5px; -webkit-border-radius: 5px;">
                        <div style="width: 100%; height: 100%; background-image: url('${response.list_imagePoster[i]}'); background-size: cover; background-position: center;"></div>
                      </div>
                      <div class="main__meta">
                        <h3>${response.list_name[i]}</h3>
                      </div>
                    </div>
                  </td>
                </tr>
              `);
            }
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
        }
        if (tableName == 'collection'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idCollection']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
          if (functionName == 'insertNewQuery'){
            $('#queryTBody').empty();
            for (let i=0; i<response.list_idProfile.length; i++){
              $('#queryTBody').append(`
                <tr onclick="$('#inputInsertNew_queryProfile').val('${response.list_idProfile[i]}');">
                  <td>
                    <div class="main__user" style="margin-bottom: 10px;">
                      <div class="main__avatar" style="min-width: 75px; height: 75px; border-radius: 5px; -webkit-border-radius: 5px;">
                        <div style="width: 100%; height: 100%; background-image: url('${response.list_imageAvatar[i]}'); background-size: cover; background-position: center;"></div>
                      </div>
                      <div class="main__meta">
                        <h3>${response.list_username[i]}</h3>
                        <span>${response.list_username_of_account[i]}</span>
                      </div>
                    </div>
                  </td>
                </tr>
              `);
            }
            console.log(response.list_idTmdb); 
          }
        }
        if (tableName == 'comments'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idComment']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'updateRecord'){
            alertMain.success({'text': response.succ_msg});
          }
        }
        if (tableName == 'countrylist'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idISO_3166_1']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
          if (functionName == 'updateRecord'){
            alertMain.success({'text': response.succ_msg});
          }
        }
        if (tableName == 'languagelist'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idISO_639_1']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
          if (functionName == 'updateRecord'){
            alertMain.success({'text': response.succ_msg});
          }
        }
        if (tableName == 'moviegenrelist'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idGenre']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
          if (functionName == 'updateRecord'){
            alertMain.success({'text': response.succ_msg});
          }
        }
        if (tableName == 'tvgenrelist'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idGenre']}`).remove();
            $('#gifLoading').hide();
          }
          if (functionName == 'insertNew'){
            window.location.reload();
          }
          if (functionName == 'updateRecord'){
            alertMain.success({'text': response.succ_msg});
          }
        }
        if (tableName == 'report'){
          if (functionName == 'drop'){
            $(`.modal .modal__btn--dismiss`).click();
            $(`#tr-${dictionary['idReport']}`).remove();
          }
          if (functionName == 'updateRecord'){
            alertMain.success({'text': response.succ_msg});
          }
        }
        console.log(response.succ_msg);
      }
      else if (response.err_msg){
        alertMain.error({'text': response.err_msg});
      }
    },
  })); 
};
