var spinner = '<div class="d-flex justify-content-center"><div class="spinner-border m-5" role="status"></div></div>';

function validateEmail(email) {
  // Регулярное выражение для проверки email адреса
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validateURL(url) {
  // Регулярное выражение для проверки URL
  const urlRegex = /^(http|https):\/\/[^ "]+$/;
  return urlRegex.test(url);
}

//======================================================================================================================
// Унифицированный показ сообщения с последующим вызовом функции
//======================================================================================================================
function show_alert(container_id='', alert_text='', timeout_function=()=>{}) {
    $("#"+container_id).text(alert_text).toggle(500).delay(2000).toggle(500);
    setTimeout(() => {  timeout_function(); }, 3000);
}

//======================================================================================================================
// Унифицированный показ сообщения об ошибке заполнения поля и прокрутка к нему
//======================================================================================================================
function show_error_input(input_id='', alert_text='') {
    $(".has_error").each(function() {
        $(this).removeClass("has_error");
    });
    $(".input_error_text").each(function() {
        $(this).remove();
    });
    $("#"+input_id).parent().addClass("has_error");
    $("#"+input_id).after('<div class="input_error_text">'+alert_text+'</div>');
    $('body').stop().animate({ scrollTop: $('#'+input_id).offset().top + $('body').scrollTop() - 100 }, 500);
//    $("#"+input_id).focus();
}

//======================================================================================================================
// Унифицированное скрытие сообщения об ошибке заполнения поля
//======================================================================================================================
function hide_error_input(input_id='') {
    if (input_id != '') {
        $("#"+input_id).parent().removeClass("has_error");
        $("#"+input_id).parent().find("input_error_text").remove();
    }
    else {
        $(".has_error").each(function() {
            $(this).find("input_error_text").remove();
            $(this).removeClass("has_error");
        });
    }
}

//======================================================================================================================
// Унифицированный AJAX-запрос
//======================================================================================================================
function PostRequest(url='', params={}, success_function=()=>{}, failure_function=()=>{}) {

    $.post(url, params, function(result) {
        if (result.ok && result.ok == 1) {
            success_function(result);
        } else {
            if (!result.error) {
                result.error = 'Ошибка'
            }
            failure_function(result);
        }
    });
}

$(document).ready(function () {
$('body').on('input', '.has_error input', function(e){
    hide_error_input($(this).attr('id'));
});
$('body').on('change', '.has_error select', function(e){
    hide_error_input($(this).attr('id'));
});
});