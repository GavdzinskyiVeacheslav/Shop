let sizeTestImage;
var images_array = [];
var minImageWidth = 1792;
var minImageHeight = 1024;

//======================================================================================================================
// Функция асинхронная, так как загрузка занимает время
//======================================================================================================================
function getImageSize(file, hebrew) {

    return new Promise((resolve, reject) => {
        sizeTestImage = new Image();
        sizeTestImage.onload = function() { resolve({ width: sizeTestImage.width, height: sizeTestImage.height }); };
        sizeTestImage.onerror = function() { reject(new Error('Не удалось загрузить изображение.')); };
        sizeTestImage.src = URL.createObjectURL(file);
    });
}

//======================================================================================================================
// Инициализация событий для обработки файлов картинок
//======================================================================================================================
function image_events_initialize({
    fileInputID='',
    success_function=()=>{},
    failure_function=()=>{},
    aspectRatio=NaN,
    hebrew=false,
}) {

    // Динамические ID диалога кроппинга и канваса
    const imageCropModal = 'image_crop_modal' + '_' + fileInputID;
    const cropImage      = 'crop_image'       + '_' + fileInputID;

    $("#"+fileInputID).change(async function(e) {

        var files = e.target.files;
        var done = function (url) {
            $("#"+fileInputID).val("");
            $("#"+cropImage).attr("src", url);
        };

        var file;
        if (files && files.length > 0) {
            file = files[0];

            if (URL) {
                done(URL.createObjectURL(file));
            } else if (FileReader) {
                let reader = new FileReader();
                reader.onload = function (e) {
                    done(reader.result);
                };
                reader.readAsDataURL(file);
            }
        }

        try {
            var size = await getImageSize(file, hebrew);
            URL.revokeObjectURL(sizeTestImage.src);
            if (size.width < minImageWidth) {
//                alert("Размеры изображения меньше разрешённых: " + minImageWidth + " х " + minImageHeight + " пикселов");
                    $("#WrongImageSizeAlert").text("Размеры изображения меньше разрешённых: " + minImageWidth + " х " + minImageHeight + " пикселов");
                    $("#WrongImageSizeAlert").toggle(600).delay(3000).toggle(600);
            } else {
                images_array.push(images_array.length);
                $("#"+imageCropModal).modal('show');
            }
            sizeTestImage.remove();
        } catch (error) {
            console.error(error.message);
        }
    });


    // Событие показа модального диалога кроппинга
    $("#"+imageCropModal).on('shown.bs.modal', function () {
        cropper = new Cropper($("#"+cropImage)[0], {
                aspectRatio: aspectRatio,
                viewMode: 3,
                autoCropArea: 1,
                scalable: false,
                zoomable: false,
                crop: function (event) {

                    const imageData = cropper.getImageData(true);
                    const cropboxData = cropper.getCropBoxData();

                    // Коэффициент масштабирования = реальная ширина / ширина DOM-объекта
                    var scaleFactor = imageData.naturalWidth / imageData.width;

                    // Реальные размеры кропа = ширина кропа * коэффициент
                    var realCropWidth = Math.round(cropboxData.width * scaleFactor);
                    var realCropHeight = Math.round(cropboxData.height * scaleFactor);

                    // Получаем размеры кропа для минимальных ширины и высоты
                    var minCropWidth = Math.round(minImageWidth / scaleFactor);
                    var minCropHeight = Math.round(minImageHeight / scaleFactor);

                    // Ограничение размера картинки + подгонка на толщину рамки кроппинга
                    // Без подгонки - зацикливание при непрерывной попытке установить размеры
                    if (realCropWidth < minImageWidth - 3 || realCropHeight < minImageHeight - 2) {
                        cropper.setData({
                            width: minImageWidth,
                            height: minImageHeight,
                        });
                    }
                }
            });
    })
    .on('hidden.bs.modal', function () {
            failure_function();
            cropper.destroy();
            cropper = null;
    });

}

function ShowCroppedImage() {

    var canvas = cropper.getCroppedCanvas({ width: minImageWidth, height: minImageHeight });
    var photo_index = images_array.length - 1;

    var newPhotoContainer = $("#PhotoContainer").clone();
    newPhotoContainer.attr("id","PhotoContainer"+photo_index);
    var newCroppedPhoto = newPhotoContainer.find("#CroppedPhoto");
    newCroppedPhoto.attr("id","CroppedPhoto"+photo_index);
    newPhotoContainer.find("#DeleteCropButton").attr("id","DeleteCropButton"+photo_index);
    newPhotoContainer.find("#CanvasImage").attr("id","CanvasImage"+photo_index).val(canvas.toDataURL("image/jpeg"));
    newPhotoContainer.find("button.delete_crop_button").attr("onclick","DeleteCroppedImage("+photo_index+");");

    newCroppedPhoto.append(canvas);
    newCroppedPhoto.find("canvas").css("width", "150px").attr("id", "CropCanvas"+photo_index);
    $(".add_photo_label").before(newPhotoContainer);
    $("#image_crop_modal_show_picture").modal('hide');
    set_file_input_disabled();

}

//======================================================================================================================
// Удалить канвас с кропом
//======================================================================================================================
function DeleteCroppedImage(photo_index, photo_id) {

    photo_exist = $("#CroppedPhoto" + photo_index).attr("data-existing_photo");

    // Скрыть DOM
//    $("#CroppedPhotoBlock" + photo_index).removeClass('d-flex').hide();
//    $("#CroppedPhotoBlock" + photo_index).remove();
    $(document).find("#PhotoContainer"+photo_index).remove();

    // Обнуление ширины и высоты canvas
//    var canvas = $("#CroppedPhoto" + photo_index + " canvas")[0];
//    if (canvas) {
//        canvas.width = 0;
//        canvas.height = 0;
//    }

    // Если команда - удалить реальную картинку, а не свежезагруженную, заполнить список для дальнейшего удаления
    if (photo_exist) {
        if (photo_id != 'undefined' && photo_id != false && photo_id != null) {
            DeletedPhotoIds.push(photo_id);
        }
        // Удалить указатель на существование фотографии
        $("#CroppedPhoto" + photo_index).removeAttr('data-existing_photo');
    }

    set_file_input_disabled();

}