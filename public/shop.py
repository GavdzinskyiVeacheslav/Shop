import base64
from datetime import datetime

from flask import render_template, request

from business.good import Good
from business.photo import Photo
from public.routes import public_bp
from utils import picture_utils
from utils.common import parse_int, categories_sections_list, cut_inject, RECORDS_PER_PAGE, get_good_ids_after_search, \
    paginate_goods, generate_pagination, return_success, process_param, return_error


@public_bp.route("/")
@public_bp.route("/goods")
def goods():
    """Главная страница с товарами"""

    # Получить запрос поиска от клиента, прогнать через защиту cut_inject()
    search = cut_inject(text=request.args.get('search', ''))

    # TODO Унести в js
    # Начинать искать товары от 3-х символов
    if len(search) < 3:
        search = ''

    # Все айдишники товаров из базы
    all_goods_ids = Good.all_goods_ids()

    # Для теста
    # amount = range(1, 25)

    # Получить список айдишников товаров, соответствующих поисковому запросу
    good_ids_after_search = get_good_ids_after_search(search, all_goods_ids)

    # Страница и кол. объявлений на странице для пагинации
    page = parse_int(request.args.get("p", 1))
    final_list_ids = paginate_goods(all_goods_ids, page)

    # Собрать объекты из айдишников
    final_list = [Good(good_id=good_id) for good_id in final_list_ids]

    # Список фотографий к каждому объявлению
    for good_item in final_list:
        good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)

    # Категории и разделы
    categories, sections = categories_sections_list()

    return render_template(
        '/goods.html',
        goods_list=final_list,
        search_filter=search,
        categories=categories,
        sections=sections,
        current_year=datetime.now().year,
        records_per_page=RECORDS_PER_PAGE,
        current_page=page,
        pagination=generate_pagination(all_goods_ids, page, final_list),

    )


@public_bp.route("/zup")
def zup():

    return render_template(
        'zup/add_photo.html',
    )


@public_bp.route("/add_photo", methods=['POST'])
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
