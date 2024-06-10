// Переменная со списком айдишников фотографий на удаление
var deletedPhotoIds = [];
// Список айдишников товаров
var productIDs = [];

//======================================================================================================================
// Добавить товар в корзину
//======================================================================================================================
function addToCart(goodId) {

    // Корзина
    let cart = $("#cart");

    // Крутануть до корзины
    $("html,body").animate({
        scrollTop: $(cart).offset().top
    });

    // Бейдж
    let bage = $("#bage");
    let bageMobile = $("#bage_mobile");

    // Обновлять количество товаров на бейдже
    let oldValue = bage.text();
    let newValue = parseInt(oldValue) + 1;
    bage.text(newValue);
    bage.addClass("badge badge_favorites");
    bageMobile.text(newValue);
    bageMobile.addClass("badge badge_favorites");

    // Записать в куку количество товаров
    Cookies.set('goodCount', newValue, { expires: 365, path: '/' });

    // Добавить id товара в список
    productIDs.push(goodId);
    // Сохраняем массив в cookie
    Cookies.set('productIDs', JSON.stringify(productIDs), { expires: 365, path: '/' });

}


//======================================================================================================================
// Добавить количество товара и показать новую сумму
//======================================================================================================================
function add_quantity(goodId) {

    // Количество
    let currentQuantity = parseInt($("#good_quantity_" + goodId).text());
    currentQuantity ++;
    $("#good_quantity_" + goodId).text(currentQuantity + ' шт');

    // Берём все цены и все количества
    let allPrices = $('.cart-item-price').text().match(/\d+/g);
    let allQuantities = $('.cart-item-quantity').text().match(/\d+/g);

    // Перемножаем элементы двух списков
    let result = allPrices.map(function(value, index) {
        return value * allQuantities[index];
    });

    // Находим сумму элементов результирующего списка
    let totalSum = result.reduce(function(accumulator, currentValue) {
        return accumulator + currentValue;
    }, 0);

    // Общая сумма
    $(".cart-total").text('Загальна сума: ' + totalSum + ' грн');
}

//======================================================================================================================
// Вычесть количество товара
//======================================================================================================================
function subtract_quantity(goodId) {

    // Количество
    let currentQuantity = parseInt($("#good_quantity_" + goodId).text());

    // Если последний товар
    if (currentQuantity == 1) {

        // Убираем div
        $("#cart-item_" + goodId).remove();

        // Обновить список id товаров для записи в куку
        let productIDs = JSON.parse(Cookies.get('productIDs'));
        let updatedProductIDs = productIDs.filter(item => item !== goodId);

        // Сохраняем массив в cookie
        Cookies.set('productIDs', JSON.stringify(updatedProductIDs), { expires: 365, path: '/' });

        // Обновить бейдж
        let bage = $("#bage");
        let bageMobile = $("#bage_mobile");

        // Обновлять количество товаров на бейдже
        let oldValue = bage.text();
        let newValue = parseInt(oldValue) - 1;
        bage.text(newValue);
        bage.addClass("badge badge_favorites");
        bageMobile.text(newValue);
        bageMobile.addClass("badge badge_favorites");

        // Записать в куку количество товаров
        Cookies.set('goodCount', newValue, { expires: 365, path: '/' });
    }

    // Если НЕ последний товар
    if (currentQuantity > 1) {
        // Отнимаем 1
        currentQuantity --;
        $("#good_quantity_" + goodId).text(currentQuantity + ' шт');
    }

    // Извлечь все числа из строки
    let allPrices = $('.cart-item-price').text().match(/\d+/g);
    let allQuantities = $('.cart-item-quantity').text().match(/\d+/g);
    let totalSum = 0;

    if (allPrices !== null) {
        // Перемножаем элементы двух списков
        let result = allPrices.map(function(value, index) {
            return parseInt(value) * allQuantities[parseInt(index)];
        });
        // Находим сумму элементов результирующего списка
        let totalSum = result.reduce(function(accumulator, currentValue) {
            return accumulator + currentValue;
        }, 0);

        // Общая сумма
        $(".cart-total").text('Загальна сума: ' + totalSum + ' грн');

    } else {
        $(".header-shop-cart").text("У кошику немає товарів");
        $(".cart-total").remove();
        Cookies.remove('productIDs');
        Cookies.remove('goodCount');
    }

}

//======================================================================================================================
// Переходим на товара передавая поиск и страницу в query_params
//======================================================================================================================
function search(page = 1) {
    const searchQuery = $('#search_request').val().trim();

    // Проверяем длину searchQuery
    if (searchQuery.length < 3) {
        alert('Введіть назву товару не менш трьох символів');
        return; // Прекращаем выполнение функции, если длина меньше трех
    }

    // Если дали что-то для поиска
    if (searchQuery) {
        const url = `/goods?search=${encodeURIComponent(searchQuery)}&p=${page}`;
        location.href = url;
    }

    // Если нажали на поиск, но ничего не ввели
    else {
        alert('Введіть назву товару');
    }
}

//======================================================================================================================
// Обработчик наведения и ухода мыши для товаров
//======================================================================================================================
function handleHover(good_id, isHover) {
    // Берём конкретный товар
    const $product = $(`#product_${good_id}`);
    // Находим описание товара внутри текущего товара
    const $description = $product.find('.description');

    if (isHover) {
        // Показываем описание и увеличиваем размер текущего товара
        $description.show();
        $product.addClass('hovered');
    } else {
        // Скрываем описание и восстанавливаем размер текущего товара
        $description.hide();
        $product.removeClass('hovered');
    }
}

$(document).ready(function() {
    // Добавляем обработчики событий для всех товаров
    $('[id^="product_"]').each(function() {
        const good_id = $(this).attr('id').split('_')[1];

        $(this).hover(
            () => handleHover(good_id, true),
            () => handleHover(good_id, false)
        );
    });
});

//======================================================================================================================
// Переход на форму заполнения данных клиента
//======================================================================================================================
function shipping_data() {

    let payment_method = $('input[name="payment"]:checked').val();

    if (!payment_method) {
        alert('Оберіть спосіб оплати')
        return;
    }

    let goodIds = []
    $('.cart-item').each(function() {
        goodIds.push($(this).data('good_id'));
    });

    PostRequest(
        url = '/pass_cart',
        params = {
            goods_quantity:    $('.cart-item-quantity').text().match(/\d+/g),
            good_prices:       $('.cart-item-price').text().match(/\d+/g),
            good_ids:          goodIds,
            payment_method:    payment_method,
        },

        success_function = function(result) {
            location.href = '/shipping_data';
        },

        failure_function = function(result) {}
    );
}

//======================================================================================================================
// Создать заказ
//======================================================================================================================
function createOrder() {

    PostRequest(
        url = '/create_order',
        params = {
            client_name:       $('#client_name').val(),
            client_phone:      $('#client_phone').val(),
            client_city:       $('#client_city').val(),
            post_office:       $('#post_office').val(),
        },

        success_function = function(result) {
            if (result.data === 'card') {
                alert('Инициализация платёжной системы');
            }
            else {
                location.href = '/my_orders';
            }
        },

        failure_function = function(result) {
            alert(result.error);
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
// Проверить куку если она есть обновить bage
//======================================================================================================================
function getCookie() {
   let goodCount = Cookies.get('goodCount');
   if (goodCount && goodCount !== 'NaN') {
    let bage = $("#bage");
    let bageMobile = $("#bage_mobile");
    bage.text(goodCount);
    bage.addClass("badge badge_favorites");
    bageMobile.text(goodCount);
    bageMobile.addClass("badge badge_favorites");
   }
}

//======================================================================================================================
// Функция для загрузки текущих значений из cookie
//======================================================================================================================
function loadProductIDs() {
    var storedProductIDs = Cookies.get('productIDs');
    if (storedProductIDs) {
        productIDs = JSON.parse(storedProductIDs);
    }
}

//======================================================================================================================
// Эта функция гарантирует, что код внутри нее будет выполняться только после загрузки всего HTML-документа
//======================================================================================================================
$(document).ready(function () {
   getCookie();
   loadProductIDs();
});



