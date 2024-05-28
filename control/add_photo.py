from flask import render_template, request
import base64

from public.routes import public_bp
from business.photo import Photo
from utils import picture_utils
from utils.common import return_success, process_param, return_error


@public_bp.route("/control")
def control():
    """Отображает страницу управления для добавления фотографий."""
    return render_template('control/add_photo.html')


@public_bp.route("control/add_photo", methods=['POST'])
def add_photo():
    """Получение и обработка данных с формы добавления фотографий"""

    # Принять словарь данных
    params = {param_item: request.form[param_item] for param_item in request.form}

    # Заполнить словарь для дальнейшей работы
    numbers = ['good_id']
    data = {}
    for number in numbers:
        data[number] = process_param(number, params, default=0, is_numeric=True)

    # Фотографии
    photos = request.form.get('photos', '')
    data['photos'] = [photo for photo in photos.split(',') if photo != 'data:image/jpeg;base64'] if photos else []

    # Фотографии
    photos = data['photos']

    try:
        for photo in photos:

            # Объект фотографии
            picture = Photo()

            # Получить следующий порядковый номер фотографии
            picture_id = picture.insert(good_id=data['good_id'])

            # Собрать путь к фотографии
            picture_path = picture_utils.picture_path(item_id=picture_id)

            # Сохранить фотографию
            with open(picture_path, 'wb') as file:
                file.write(base64.b64decode(photo))

            # Получаем ширину и высоту из одной функции Pillow
            width, height = picture_utils.get_picture_sizes(item_id=picture_id)

            # Обновляем размеры для каждой фотографии
            picture.update(
                width=width,
                height=height,
            )

    except Exception as ex:
        # Показать ошибку
        return return_error(error=f'{ex}')

    # Сохранение фотографий к товару прошло успешно --> обновляем страницу
    return return_success()
