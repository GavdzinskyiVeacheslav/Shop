//======================================================================================================================
// Установить фильтр по категории
//======================================================================================================================
var DeletedPhotoIds = []

function set_category_filter(category_id) {

     $('#section_list')
        .empty()
        .html(spinner);

    PostRequest(
        url = '/list_section_by_category',
        params = {
            category_id: category_id,
        },
        success_function = function(result) {
            if ($('#category_list').val() == 0) {
                $('#section_list').empty().append('<option value="0">Выберите раздел</option>').prop('disabled', true);
            } else {
                $('#section_list').prop('disabled', false);
                $('#section_list').html(result.data);
            }
        }
    );
}

//======================================================================================================================
// Добавление объявления
//======================================================================================================================
async function create_ad() {

    if (validateEmail($('#owner_email').val()) == false) {
        show_error_input("owner_email", 'Указана некорректный e-mail');
        return false;
    }

    $('.loader_holder').fadeIn();
    $('.button_spinner').css("display","inline-block");
    $('#add_ad_button').prop('disabled',true);

    let photos_amount = images_array.length;
    let canvas = [];
    let imageBlob = [];

    let j = 0;
    $('#AllPhotos canvas').each(function(i) {
        if ($(this).width) {
            canvas[j] = $(this);
            imageBlob[j] = $(this).parent().find("input.CanvasImage").val();
            j++;
        }
    });

    let formData = new FormData();
    formData.append("client_id", $("#client_id").val());
    formData.append("section_id", $("#section_list").val());
    formData.append("category_id", $("#category_list").val());
    formData.append("owner_name", $("#owner_name").val());
    formData.append("city", $("#city").val());
    formData.append("city_name", $("#city_name").val());
    formData.append("owner_phone", $("#owner_phone").val());
    formData.append("owner_email", $("#owner_email").val());
    formData.append("ad_text", $("#ad_text").val());
    formData.append("expire", $("#expire").val());
    formData.append("photos", imageBlob);

    let response = await fetch('/create_ad_post', {
        method: 'POST',
        body: formData
    });

    let result = await response.json();
    if (result.ok == 1) {
            location.href = "/created_ad";
    } else {
        $('.loader_holder').fadeOut();
        $('.button_spinner').css("display","none");
        $('#add_ad_button').prop('disabled',false);
        if (!result.error) result.error = 'Ошибка'; {
            if (result.data) {
                switch (result.data) {
                    case 'category':
                        show_error_input("category_list", result.error);
                    break;
                    case 'section':
                        show_error_input("section_list", result.error);
                    break;
                    case 'name':
                        show_error_input("owner_name", result.error);
                    break;
                    case 'city':
                        show_error_input("city", result.error);
                    break;
                    case 'phone':
                        show_error_input("owner_phone", result.error);
                    break;
                    case 'text':
                        show_error_input("ad_text", result.error);
                    break;
                    default:
                        show_alert( 'add_ad_alert', result.error);
                }
            }
            else {
                show_alert('add_ad_alert', result.error);
            }
        }
    }
}

//======================================================================================================================
// Ограничивает количество добавляемых фотографий, не больше (10)
//======================================================================================================================
function set_file_input_disabled() {
    var amount = $("#AllPhotos [data-existing_photo]").length;
    $("#show_picture").attr('disabled', amount > 9 ? true : false);
    if (amount < 10) {
        $('.add_photo_label').css("display","flex");
        $('.AllPhotosMaxMessage').css("display","none");
    }
    else {
        $('.add_photo_label').css("display","none");
        $('.AllPhotosMaxMessage').css("display","block");
    }
}

//======================================================================================================================
// Изменение объявления
//======================================================================================================================
async function edit_ad() {

    if (validateEmail($('#owner_email').val()) == false) {
        show_error_input("owner_email", 'Указана некорректный e-mail');
        return false;
    }

    $('.loader_holder').fadeIn();
    $('.button_spinner').css("display","inline-block");
    $('#add_edit_button').prop('disabled',true);

    let photos_amount = images_array.length;
    let canvas = [];
    let imageBlob = [];

    // Добавление нескольких канвасов
    let j = 0;
    for (let i = 0; i < photos_amount; i++) {
        if ( $("#CroppedPhoto" + i + " canvas")[0] && $("#CroppedPhoto" + i + " canvas")[0].width) {
            canvas[j] = $("#CroppedPhoto" + i + " canvas")[0];
            imageBlob[j] = $("#CanvasImage" + i).val();
            j++;
        }
    }

    let formData = new FormData();
    formData.append("ad_id", $("#ad_id").val());
    formData.append("client_id", $("#client_id").val());
    formData.append("section_id", $("#section_list").val());
    formData.append("category_id", $("#category_list").val());
    formData.append("owner_name", $("#owner_name").val());
    formData.append("city", $("#city").val());
    formData.append("city_name", $("#city_name").val());
    formData.append("owner_phone", $("#owner_phone").val());
    formData.append("owner_email", $("#owner_email").val());
    formData.append("ad_text", $("#ad_text").val());
    formData.append("deleted_photo_ids", DeletedPhotoIds);
    formData.append("photos", imageBlob);

    let response = await fetch('/edit_ad/' + $("#ad_id").val(), {
        method: 'POST',
        body: formData
    });


    let result = await response.json();
    if (result.ok == 1) {
        if (result.data > 0) {
           location.reload();
        } else {
            location.href = "/my_ads";
        }
    } else {
        $('.loader_holder').fadeOut();
        $('.button_spinner').css("display","none");
        $('#add_edit_button').prop('disabled',false);
        if (!result.error) result.error = 'Ошибка'; {
            if (result.data) {
                switch (result.data) {
                    case 'category':
                        show_error_input("category_list", result.error);
                    break;
                    case 'section':
                        show_error_input("section_list", result.error);
                    break;
                    case 'name':
                        show_error_input("owner_name", result.error);
                    break;
                    case 'city':
                        show_error_input("city", result.error);
                    break;
                    case 'phone':
                        show_error_input("owner_phone", result.error);
                    break;
                    case 'text':
                        show_error_input("ad_text", result.error);
                    break;
                    default:
                        show_alert('add_edit_alert', result.error);
                }
            }
            else {
                show_alert('add_edit_alert', result.error);
            }
        }
    }
}

//======================================================================================================================
// Добавление уже существующих фотографий в общий список
//======================================================================================================================
function fill_image_array(){
      $("[data-existing_photo = '1']")
      .each(function( i ) {
        images_array.push(i);
      });
}

//======================================================================================================================
// Установка обработчика для кнопки Удалить объявления
//======================================================================================================================
function set_delete_ad_handler(ad_id) {
    $("#delete_ad_button").click(function() {
        $(this).find('.button_spinner').css("display","inline-block");
        $('#delete_ad_button').prop('disabled',true);
        delete_ad(ad_id);
    });
}

//======================================================================================================================
// Удаление объявления
//======================================================================================================================
function delete_ad(ad_id) {

    // Почистить из куки
    let from_cookie = $.cookie('favourite_list');
    if (from_cookie) {
        favourite_list = JSON.parse(from_cookie);
    }
    delete favourite_list['ad' + ad_id];
    $.cookie('favourite_list', JSON.stringify(favourite_list), { expires: 365, path: '/' });

    PostRequest(
        url = '/delete_ad',
        params = { ad_id: ad_id },
        success_function = function(result) {
            location.reload();
        },
         failure_function = function(result) {
            if (!result.error) result.error = 'Ошибка';
            alert(result.error);
            $('.loader_holder').fadeOut();
            $('.button_spinner').css("display","none");
            $('#delete_ad_button').prop('disabled',false);
            show_alert( 'delete_ad_alert', result.error);
        }
    );
}

//======================================================================================================================
// Список разделов по выбору категорий
//======================================================================================================================
function sections_list(category_id) {

    $('#section_list')
       .empty()

    PostRequest(
        url = '/list_section_by_category',
        params = {
            category_id: category_id,
        },
        success_function = function(result) {
            if ($('#category_list').val() == 0) {
                $('#section_list').append('<option value="0">Выберите раздел</option>').prop('disabled', true);
            } else {
                $('#section_list').prop('disabled', false);
                $('#section_list').html(result.data);
            }
        }
    );
}

//======================================================================================================================
// Установить фильтр на поиск объявлений
//======================================================================================================================
function set_ads_filter(page=1) {
    var search_request = $('#search_request').val();
    var city_ids = $(".cities:checked").map(function() { return $(this).val(); }).get();

    const queryString = window.location.pathname.split('/').filter(element => element !== "");
    const category = queryString[0] !== 'ads' ? queryString[0] : '';
    const section = queryString[1] || '';

    const queryParams = new URLSearchParams();

    if (search_request) queryParams.append('search', search_request);
    if (city_ids.length) queryParams.append('city', city_ids.join(','));
    queryParams.append('p', page);

    const url = category && category !== 'ads'
        ? `/${category}/${section}?${queryParams}`
        : `/ads?${queryParams}`;

    location.href = url;
}

//======================================================================================================================
// Сбросить выбранные города
//======================================================================================================================
function refresh_city_filter() {
    $(".cities:checked").each(function() {
        $(this).prop("checked", false);
    });
    set_ads_filter();
}

//======================================================================================================================
// Очистить введенный фильтр
//======================================================================================================================
function clear_search_filter(x) {
        if(x == 1){
          $('#search_request').val('');
       }else{
          $('#city_id').val(0);
       }
    set_ads_filter();
}

//======================================================================================================================
// Установка количества объявлений на странице
//======================================================================================================================
function set_records_per_page(records_amount, page=1) {

    PostRequest(
        url = '/ads/set_records_per_page',
        params = { records_amount: records_amount },
        success_function = function(result) {
            location.reload();
        }
    );
}

//======================================================================================================================
// Галерея
//======================================================================================================================
function changeImage(photo_id, ad_id) {
    const mainImage = $("#main_image" + ad_id);
    const prevImage = $("#image"+ photo_id);
    const srcPrevImage = prevImage.attr('src');
    const new_path = srcPrevImage;
    mainImage.attr("src", new_path);
    $(".ad_photo_big_background_blur").css("background-image","url("+new_path+")");
}


function expandAdDesc() {
  $('.ad-desc').each(function(index, adDesc) {
    adDesc = $(adDesc);
    var maxHeight = parseInt(adDesc.css('max-height'), 10);
    adDesc.css('overflow', 'hidden');
    if (adDesc.prop('scrollHeight') > maxHeight) {
      var toggleButton = $('<div class="toggleButton"></div>');
      toggleButton.css('background', 'linear-gradient(180deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0))');
      var btn_exp = $('<a class="btn-exp" href="#">Показать полностью</a>');
      adDesc.after(toggleButton);
      toggleButton.append(btn_exp);
      var isCollapsed = true;
      btn_exp.click(function(e) {
        e.preventDefault();
        if (isCollapsed) {
          adDesc.animate({maxHeight: adDesc.prop('scrollHeight')}, 500);
          toggleButton.css('background', '');
          btn_exp.text('Скрыть');
        } else {
          adDesc.animate({maxHeight: maxHeight}, 500);
          toggleButton.css('background', 'linear-gradient(180deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0))');
          btn_exp.text('Показать полностью');
        }
        isCollapsed = !isCollapsed;
      });
    }
  });
}


//======================================================================================================================
// Если клиент авторизован - Добавить/Убрать избранное в базу иначе, говорим клиенту авторизоваться. Обновляем badge
//======================================================================================================================
function toggleFavourite(ad_id, flag, isUserAuthenticated) {
    // Клиент авторизован
    if (isUserAuthenticated) {
        if (flag === 0) {
            // Убрать
            $('.rem_fav' + ad_id).addClass('d-none');
            $('.ad_fav' + ad_id).removeClass('d-none');
        } else {
            // Добавить
            $('.rem_fav' + ad_id).removeClass('d-none');
            $('.ad_fav' + ad_id).addClass('d-none');
        }

        // Записать в базу(redis)
        let url = flag === 0 ? '/remove_favourite' : '/add_to_favourite';
        PostRequest(
            url,
            {
                favourite_ad_id: ad_id,
            },
            success_function = function(result) {
                $('.badge_favorites').each(function() {
                    if (result.data > 0) {
                        $(this).removeClass("d-none");
                    } else {
                        $(this).addClass("d-none");
                    }
                    $(this).html(result.data);
                });
            },
            failure_function = function(result) {
                if (!result.error) result.error = 'Ошибка';
                show_alert('add_to_favourite_alert', result.error);
            }
        );
    // Клиент НЕ авторизован
    } else {
        alert('Авторизуйтесь чтобы добавить в избранное');
    }
}

//======================================================================================================================
// Показать избранные
//======================================================================================================================
function show_favorites() {

    // Из redis
    PostRequest(
        url = '/get_favorites_list',
        params = {},
        success_function = function(result) {
            if (result.data) {
                $.each(result.data, function(index, value) {
                    $('.add_to_favorite_button.ad_fav' + value).addClass('d-none');
                    $('.rem_fav' + value).removeClass('d-none');
                });
                $('.badge_favorites').each(function() {
                    if (result.data.length > 0) {
                        $(this).removeClass("d-none");
                    } else {
                        $(this).addClass("d-none");
                    }
                    $(this).html(result.data.length);
                });
            }
        },
        function(result) {},
    );
}


$(document).ready(function () {

//    fill_image_array();
//    show_favorites();

    $('body').on('click', '.mobile_select_city_confirm_button', function(e){
        set_ads_filter();
    });

});
