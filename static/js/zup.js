//======================================================================================================================
// Добавить фотографии к товару
//======================================================================================================================
async function add_photo() {

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
    formData.append("good_id", $("#good_id").val());
    formData.append("photos", imageBlob);

    let response = await fetch('/control/add_photo', {
        method: 'POST',
        body: formData
    });

    let result = await response.json();
    if (result.ok == 1) {
            location.reload();
    } else {
        show_alert('add_photos_alert', result.error);
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
// Инициализация события для кроппера
//======================================================================================================================
//fill_image_array();
set_file_input_disabled();
$(document).ready(function () {
    image_events_initialize({
      fileInputID: "show_picture"
    });
});