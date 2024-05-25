from datetime import datetime

from flask import render_template, request, session

from business.good import Good
from business.order import Order
from public.routes import public_bp
from utils import common
from utils.common import parse_int, categories_sections_list


@public_bp.route("/")
@public_bp.route("/goods")
def goods():
    """Главная страница с товарами"""

    all_goods_ids = Good.all_goods_ids()
    goods_list = [Good(good_id=good_id) for good_id in all_goods_ids]

    # goods_list = range(1, 100)

    # Категории и разделы
    categories, sections = categories_sections_list()

    return render_template(
        '/goods.html',
        goods_list=goods_list,
        search_filter='',
        client_name='Имя клиента',
        client_email='Email клиента',
        verified_email=1,
        google_client=0,
        authorize=session.get('client.logged_in', None),
        categories=categories,
        sections=sections,
        city_ids=[],
        current_year=datetime.now().year,
        # records_per_page=records_per_page,
        current_page=parse_int(request.args.get("p", 1)),
    )

    # Пример
    # new_order = Order()
    #
    # new_order.insert(
    #     name='first_test',
    #     description='text text text'
    # )
    #
    # return 'GO'
    # Принять словарь данных

    # Пример
    # params = {param_item: request.args[param_item] for param_item in request.args}
    #
    # # Заполнить словарь для дальнейшей работы
    # strings = ['city', 'search']
    # data = {}
    # for string in strings:
    #     data[string] = process_param(string, params)
    #
    # # Начинать искать объявления от 3-х символов
    # if len(data['search']) < 3:
    #     data['search'] = ''
    #
    # # Айдишники городов
    # city_ids = [int(city_id) for city_id in data['city'].replace(',', ' ').split()]
    #
    # Все ID объявлений разрешённых к публикации включая(учитывая) фильтр(можно выбрать сразу несколько городов)
    # all_ad_ids = Ad.set_ads_filter(city_ids=city_ids, content=data['search'])
    #
    # # Айдишники платных объявлений из кеша (redis) LISTS включая (учитывая) фильтр
    # paid_ad_ids = Ad.paid_ads(city_ids=city_ids, content=data['search'], service=AT_THE_TOP_OF_THE_MAIN)
    #
    # # (Неоплаченные объявления) Упорядочить set по убыванию - отображать сначала последние добавленные объявления
    # unpaid_ad_ids = sorted(all_ad_ids - set(paid_ad_ids), reverse=True)
    #
    # Страница и кол. объявлений на странице для пагинации
    # page = parse_int(request.args.get("p", 1))
    # records_per_page = int(session['records_per_page']) if 'records_per_page' in session else 12
    #
    # # Финальный список с пагинацией
    # start_position = (page - 1) * records_per_page
    # final_list_ids = (shuffle_list(paid_ad_ids) + unpaid_ad_ids)[start_position:start_position + records_per_page]
    #
    # # Список объектов объявлений
    # final_list = [Ad(ads_id=ad_id) for ad_id in final_list_ids]
    #
    # # Список фотографий к каждому объявлению
    # for ad_item in final_list:
    #     ad_item.photos = Photo.photo_ids_list(ad_id=ad_item.id)
    #
    # # Клиент
    # client_item = Client(client_id=session.get('client.client_id', ''))

    # Пагинация - количество объявлений на странице
    # records_per_page = int(session['records_per_page']) if 'records_per_page' in session else 12

    # Категории и разделы
    # categories, sections = categories_sections_list()
    #
    # return render_template(
    #     '/goods.html',
    #     search_filter='',
    #     goods_list=goods_list,
    #     client_name='Имя клиента',
    #     client_email='Email клиента',
    #     verified_email=1,
    #     google_client=0,
    #     authorize=session.get('client.logged_in', None),
    #     categories=categories,
    #     sections=sections,
    #     city_ids=[],
    #     current_year=datetime.now().year,
    #     records_per_page=records_per_page,
    #     current_page=parse_int(request.args.get("p", 1)),
    #     pagination=common.pagination(
    #         total_amount=len(all_goods_ids),
    #         amount_per_page=records_per_page,
    #         current_page=parse_int(request.args.get("p", 1)),
    #         template_path='/paginator.html',
    #     ) if final_list else '',
    # )
