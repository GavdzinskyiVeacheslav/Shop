import json
import urllib.parse

from flask import render_template, request

from business.category import Category
from business.good import Good
from business.photo import Photo
from business.section import Section
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


@public_bp.route("/good_page/<int:good_id>")
def good_page(good_id):
    """Страница конкретного товара"""

    # Получить товар
    good_item = Good(good_id=parse_int(good_id))

    # Товар не найден отдаём 404
    if not good_item.id:
        return render_template(
            '/public/404.html',
        )

    # Список фотографий к объявлению
    good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)

    return render_template(
        '/public/good_page.html',
        good_item=good_item,
    )


@public_bp.route('/<category>/', defaults={"section": ''})
@public_bp.route('/<category>/<section>/')
def section_list(category, section):
    """Переход по названию категории или раздела"""

    # Отдать 404 если передали несуществующую категорию или раздел
    category_item = Category.get_category_by_folder(category)
    if not category_item:
        return render_template(
            '/404.html',
        )

    if section:
        section_item = Section.get_section_by_folder(section)
        if not section_item:
            return render_template(
                '/404.html',
            )
    else:
        section_item = 0

    # Отфильтровать по категории или разделу в зависимости от того что пришло
    filtered_good_ids = []

    # Фильтр по категории
    if category_item.id:
        good_ids_by_category = Good.get_ids_by_category(category_id=category_item.id)
        filtered_good_ids = good_ids_by_category

    # Фильтр по разделу
    if section:
        good_ids_by_section = Good.get_ids_by_section(section_id=section_item.id if section else 0)
        filtered_good_ids = good_ids_by_section

    # Страница и кол. объявлений на странице для пагинации
    page = parse_int(request.args.get("p", 1))
    final_list_ids = paginate_goods(filtered_good_ids, page)

    # Собрать объекты
    final_list = [Good(good_id=good_id) for good_id in filtered_good_ids]

    # Список фотографий к каждому объявлению
    for good_item in final_list:
        good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)

    return render_template(
        '/public/goods.html',
        goods_list=final_list,
        records_per_page=RECORDS_PER_PAGE,
        current_page=page,
        pagination=generate_pagination(filtered_good_ids, page, final_list),
    )


@public_bp.route("/shop_cart")
def shop_cart():
    """Корзина"""

    # Неизменяемый словарь кук
    data = request.cookies

    # Извлечь значения из ImmutableMultiDict
    good_count = parse_int(data.get('goodCount'))
    good_ids_encoded = data.get('productIDs')

    # Инициализация нужных переменных
    good_items = []
    quantity = 0
    total_sum = 0

    # Если кука не пустая
    if good_ids_encoded:

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
