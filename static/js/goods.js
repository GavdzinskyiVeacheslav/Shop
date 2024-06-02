// Уже используем
//======================================================================================================================
// Переходим на товара передавая поиск и страницу в query_params
//======================================================================================================================
function search(page = 1) {
    const searchQuery = $('#search_request').val().trim();

    // Проверяем длину searchQuery
    if (searchQuery.length < 3) {
        alert('Введите название товара не менее трех символов');
        return; // Прекращаем выполнение функции, если длина меньше трех
    }

    // Если дали что-то для поиска
    if (searchQuery) {
        const url = `/goods?search=${encodeURIComponent(searchQuery)}&p=${page}`;
        location.href = url;
    }

    // Если нажали на поиск, но ничего не ввели
    else {
        alert('Введите название товара');
    }
}

//======================================================================================================================
// Показывает описание и увеличивает карточку товара при наведении
//======================================================================================================================
function start_hover(good_id) {
    // Берём конкретный товар
    const $product = $('#product_' + good_id);
    // Находим описание товара внутри текущего товара
    const $description = $product.find('.description');

    // Добавляем обработчик события для наведения мыши
    $product.on('mouseenter', function() {
        // Показываем описание товара
        $description.show();
        // Увеличиваем размер текущего товара
        $product.css('transform', 'scale(1.05)');
    });
}


//======================================================================================================================
// Скрывает описание и возвращает размер карточки товара при mouseleave
//======================================================================================================================
function end_hover(good_id) {
    // Берём конкретный товар
    const $product = $('#product_' + good_id);
    // Находим описание товара внутри текущего товара
    const $description = $product.find('.description');

    // Добавляем обработчик события для ухода мыши с элемента
    $product.on('mouseleave', function() {
        // Скрываем описание товара
        $description.hide();
        // Восстанавливаем размер текущего товара
        $product.css('transform', 'scale(1)');
    });
}


// Примеры на потом //
var DeletedPhotoIds = []
//======================================================================================================================
// Установить фильтр по категориям
//======================================================================================================================
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
// Добавление уже существующих фотографий в общий список
//======================================================================================================================
function fill_image_array(){
      $("[data-existing_photo = '1']")
      .each(function( i ) {
        images_array.push(i);
      });
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
// Сбросить выбранные города
//======================================================================================================================
function refresh_city_filter() {
    $(".cities:checked").each(function() {
        $(this).prop("checked", false);
    });
    set_ads_filter();
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
// Эта функция гарантирует, что код внутри нее будет выполняться только после загрузки всего HTML-документа
//======================================================================================================================
$(document).ready(function () {
    // Вызовы функций
});



