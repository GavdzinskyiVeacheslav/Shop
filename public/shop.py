import json
import urllib.parse

from flask import render_template, request, session

from business.category import Category
from business.good import Good
from business.photo import Photo
from business.section import Section
from public.routes import public_bp
from utils.common import (parse_int, cut_inject, RECORDS_PER_PAGE, get_good_ids_after_search, paginate_goods,
                          generate_pagination, find_duplicates, return_success, return_error)


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


@public_bp.route("/pass_cart", methods=['POST'])
def pass_cart():
    """Передать корзину дальше"""

    # Берём данные с формы
    data = request.form

    # Extract values from the ImmutableMultiDict
    goods_quantity = data.getlist('goods_quantity[]')
    good_prices = data.getlist('good_prices[]')
    good_ids = data.getlist('good_ids[]')
    payment_method = cut_inject(text=data.get('payment_method'))

    # Convert the lists to a more structured form if needed
    goods_to_pass = [
        {'id': gid, 'quantity': qty, 'price': price}
        for gid, qty, price in zip(good_ids, goods_quantity, good_prices)
    ]

    # Записать в сессию
    session['goods'] = goods_to_pass
    session['payment_method'] = payment_method

    # Переходим на заполнение формы
    return return_success()


@public_bp.route("/shipping_data")
def shipping_data():
    """Форма для заполнения данных клиента"""

    # Достать данные из сессии
    goods_from_session = session['goods']
    payment_method = session['payment_method']

    # Достать только айдишники
    good_ids = [int(item['id']) for item in goods_from_session]

    # Количество
    quantity = {int(item['id']): int(item['quantity']) for item in goods_from_session}

    # Сделать объекты
    good_items = [Good(good_id=good_id) for good_id in good_ids]

    # Динамически создадим новый атрибут, запишем в него цену учитывая количество
    for good_item in good_items:
        good_item.multiple_price = good_item.price * quantity.get(good_item.id, 1)

    # Общая сумма учитывая количество товаров
    total_sum = sum([good_item.multiple_price for good_item in good_items])

    # Список фотографий к каждому объявлению
    for good_item in good_items:
        good_item.photos = Photo.all_photo_items_by_good(good_id=good_item.id)

    return render_template(
        '/public/shipping_data.html',
        good_items=good_items,
        payment_method=payment_method,
        total_sum=total_sum,
        quantity=quantity,
    )


@public_bp.route("/create_order", methods=['POST'])
def create_order():
    """Создать заказ"""

    # Данные из формы
    data = request.form

    # Проверка на пустые поля и cut_inject на заполненные
    client_name = cut_inject(text=data.get('client_name'))
    if not client_name:
        return return_error(error="Заповніть ім'я прізвище та по батькові")
    client_phone = cut_inject(text=data.get('client_phone'))
    if not client_phone:
        return return_error(error="Заповніть номер телефону")
    client_city = cut_inject(text=data.get('client_city'))
    if not client_city:
        return return_error(error="Заповніть місто")
    post_office = cut_inject(text=data.get('post_office'))
    if not post_office:
        return return_error(error="Заповніть Відділення Нової Пошти")

    # Данные из сессии
    goods_from_session = session['goods']
    payment_method = session['payment_method']

    # Сделать нужные строки
    ids = ",".join(item['id'] for item in goods_from_session)
    prices = ",".join(item['price'] for item in goods_from_session)
    quantities = ",".join(item['quantity'] for item in goods_from_session)



    return return_success(data=payment_method)


@public_bp.route("/my_orders")
def my_orders():
    """Заказы клиента"""
    return render_template(
        '/public/orders.html',
        orders_page=True,
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
