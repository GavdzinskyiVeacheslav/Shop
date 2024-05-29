from datetime import datetime

from flask import render_template, request

from business.good import Good
from business.photo import Photo
from public.routes import public_bp
from utils.common import (parse_int, categories_sections_list, cut_inject, RECORDS_PER_PAGE, get_good_ids_after_search,
                          paginate_goods, generate_pagination)


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
