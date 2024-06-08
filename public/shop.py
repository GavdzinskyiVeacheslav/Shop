import json
import urllib.parse

from flask import render_template, request

from business.good import Good
from business.photo import Photo
from public.routes import public_bp
from utils.common import (parse_int, cut_inject, RECORDS_PER_PAGE, get_good_ids_after_search, paginate_goods,
                          generate_pagination, find_duplicates)


@public_bp.route("/")
@public_bp.route("/goods")
def goods():
    """Главная страница с товарами"""

    # Получить запрос поиска от клиента, прогнать через защиту cut_inject()
    search = cut_inject(text=request.args.get('search', ''))

    # Все айдишники товаров из базы
    all_goods_ids = Good.all_goods_ids()

    # Получить список айдишников товаров, соответствующих поисковому запросу
    good_ids_after_search = get_good_ids_after_search(search, all_goods_ids)

    # Страница и кол. объявлений на странице для пагинации
    page = parse_int(request.args.get("p", 1))
    final_list_ids = paginate_goods(good_ids_after_search, page)

    # Собрать объекты из айдишников
    final_list = [Good(good_id=good_id) for good_id in final_list_ids]

    # Список фотографий к каждому объявлению
    for good_item in final_list:
        good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)

    return render_template(
        '/public/goods.html',
        goods_list=final_list,
        search_filter=search,
        records_per_page=RECORDS_PER_PAGE,
        current_page=page,
        pagination=generate_pagination(all_goods_ids, page, final_list),
    )


# TODO создать раут для перехода на страницу товара
# """Страница конкретного товара"""
# TODO 1. Сделать новый раут в shop.py этот раут будет динамический и он будет для показа конкретного товара назвать
#  например /good_page/<int:good_id>  - если тяжело посмотреть информацию про динамические рауты flask.
#    1.1 Внутри раута должен собираться объект данного товара и передаваться дальше в шаблон.
#    1.2  # Список фотографий к товару
#         for good_item in final_list:
#         good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)
#    и передаваться дальше в шаблон.
#    1.3 Если передали id которого у нас нет в базе нужно показать кастомный шаблон 404 -
#     1.4 Пусть этот раут возвращает good_page.html в котором должен сохраниться header и footer как на
#     главной странице но середина должна показывать: Галерею фотографий полное описание всю нужную информацию и кнопку
#     купить.


# TODO создать раут который будет обрабатывать приём категории и раздела
# """Переход по названию категории или раздела"""
#     # TODO Отдать 404 если передали несуществующую категорию или раздел
#
#     # TODO Отфильтровать таким образом что если пришла категория то все товары по категории,
#     #  если пришла категория и раздел то все товары только по этой категории и по этому разделу
#     filtered_list_ids = []
#
#     # TODO Страница и кол. объявлений на странице для пагинации
#
#     # TODO собрать объекты
#     final_list = []
#
#     # TODO Список фотографий к каждому объявлению
#
#     # TODO Категории и разделы
#
#     # TODO Добавить js для обработки такого раута или добавить в тот который фильтрует по названию товара
#
#    render template возвращает good.html и нужные для работы переменные


@public_bp.route("/test")
def test():
    good_item = Good(good_id=2)
    good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)
    return render_template(
        '/public/good_page.html',
        good_item=good_item,
    )


@public_bp.route("/shop_cart")
def shop_cart():
    """Корзина"""

    # Неизменяемый словарь кук
    data = request.cookies

    # Извлечь значения из ImmutableMultiDict
    good_count = parse_int(data.get('goodCount'))
    good_ids_encoded = data.get('productIDs')

    # Декодировать строку
    good_ids_decoded = urllib.parse.unquote(good_ids_encoded)

    # Преобразовать строку в список
    good_ids = json.loads(good_ids_decoded)

    # Количество каждого товара
    quantity = find_duplicates(good_ids)

    # Собрать объекты товаров
    good_items = [Good(good_id=good_id) for good_id in list(set(good_ids))]

    # Динамически создадим новый атрибут, запишем в него цену учитывая количество
    for good_item in good_items:
        good_item.multiple_price = good_item.price * quantity.get(good_item.id, 1)

    # Общая сумма учитывая количество товаров
    total_sum = sum([good_item.multiple_price for good_item in good_items])

    # Список фотографий к каждому объявлению
    for good_item in good_items:
        good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)

    return render_template(
        '/public/shop_cart.html',
        good_count=good_count,
        good_items=good_items,
        quantity=quantity,
        total_sum=total_sum,
        shop_cart_page=True,
    )


@public_bp.route("/delivery")
def delivery():
    """Доставка"""
    return render_template(
        '/public/info/delivery.html',
    )


@public_bp.route("/warranty_and_returns")
def warranty_and_returns():
    """Гарантия и возврат"""
    return render_template(
        '/public/info/warranty_and_returns.html',
    )


@public_bp.route("/contacts")
def contacts():
    """Контакты"""
    return render_template(
        '/public/info/contacts.html',
    )


@public_bp.route("/feedback")
def feedback():
    """Отзывы"""
    return render_template(
        '/public/info/feedback.html',
    )
