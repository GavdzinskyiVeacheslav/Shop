import decimal
import re

from flask import render_template

from business.category import Category
from business.good import Good
from business.section import Section

# Константа для количества товаров на странице
RECORDS_PER_PAGE = 12


def get_good_ids_after_search(search, all_goods_ids):
    """Получить список айдишников товаров после поиска"""
    if search:
        goods_by_search = Good.good_ids_by_search(search=search)
        return set(all_goods_ids).intersection(set(goods_by_search))
    return set(all_goods_ids)


def paginate_goods(good_ids, page):
    """Пагинация товаров"""
    start_position = (page - 1) * RECORDS_PER_PAGE
    return list(good_ids)[start_position:start_position + RECORDS_PER_PAGE]


def generate_pagination(all_goods_ids, page, final_list):
    """Генерация данных для пагинации"""
    return pagination(
        total_amount=len(all_goods_ids),
        amount_per_page=RECORDS_PER_PAGE,
        current_page=page,
        template_path='/paginator.html',
    ) if final_list else ''


def categories_sections_list():
    """Списки категорий и разделов"""

    categories = Category.all_categories()
    sections = {}
    for category in categories:
        sections[category.id] = Section.list_section_by_category(category_id=category.id)

    return categories, sections


def parse_int(value: any = None) -> int:
    """Защита на ввод числа"""
    if not value:
        return 0

    value_type = type(value)
    # print(value_type)
    # if value_type is not str and value_type is not int and value_type is not float and value_type is not bool:
    if value_type not in (str, int, float, bool, decimal.Decimal):
        return 0

    if value_type is int:
        return value

    if value_type is float:
        return int(float(value))

    if value_type is decimal.Decimal:
        return int(float(value))

    if value_type is bool:
        return 1 if value else 0

    if value_type is str:
        value = value.strip()

        try:
            value = int(float(value))
            return value
        except ValueError:
            return 0
        except Exception:
            # print(ex)
            return 0
    return 0


def cut_inject(text=''):
    """Определяет и вырезает тег <script> и слово select из основного текста для защиты от XSS атак"""

    # В случае когда есть открывающийся и закрывающийся тег <script>
    regex = r"<\s*script\s*>(.*?)<\s*/\s*script\s*>"
    found = re.search(regex, text)
    if found:
        text = re.sub(regex, '', text, flags=re.S)

    # В том случае когда есть только открывающийся тег <script>
    regex = r"<\s*script\s*>(.*?)$"
    found = re.search(regex, text)
    if found:
        text = re.sub(regex, '', text, flags=re.S)

    # В случае когда пытаются использовать слово select
    regex = r"select(.*?)$"
    found = re.search(regex, text, flags=re.I)
    if found:
        text = re.sub(regex, '', text, flags=re.S | re.I)

    return text


def process_param(param_name: str, params: dict, default='', is_numeric=False):
    """cut_inject и parse_int в одной функции"""
    value = params.get(param_name, default)
    cleaned_value = cut_inject(text=str(value)).strip()
    return parse_int(cleaned_value) if is_numeric else cleaned_value


def pagination(total_amount=0, amount_per_page=0, current_page=1, template_path=''):
    """Получение набора данных для пагинатора"""

    if total_amount == 0 or amount_per_page == 0:
        return {}
    if not template_path:
        return {}

    # Количество страниц
    if total_amount // amount_per_page == total_amount / amount_per_page:
        pages_amount = int(total_amount / amount_per_page)
    else:
        pages_amount = int(total_amount // amount_per_page + 1)

    if current_page > pages_amount:
        current_page = pages_amount

    # Формируем данные
    data = {
        'first_disabled': current_page == 1,
        'prev_disabled': current_page == 1,
        'prev_number': current_page - 1,
        'next_disabled': current_page == pages_amount,
        'next_number': current_page + 1,
        'last_disabled': current_page == pages_amount,
        'last_number': pages_amount,
        'amount_per_page': amount_per_page,
    }

    # Первая и последня кнопки
    if pages_amount > 5:
        if current_page < 4:
            first_number = 1
            last_number = 5
        elif current_page > pages_amount - 2:
            first_number = pages_amount - 4
            last_number = pages_amount
        else:
            first_number = current_page - 2
            last_number = current_page + 2
    else:
        first_number = 1
        last_number = pages_amount

    pages = []
    for i in range(first_number, last_number + 1):

        # Если страницы кончились
        if pages_amount < i:
            break

        pages.append({
            'number': i,
            'active': current_page == i,
            'disabled': current_page == i,
        })
    data['pages'] = pages

    return render_template(
        template_path,
        data=data,
    )


def return_success(ok=1, error='', data=None):
    return {
        'success': 1,
        'ok': ok,
        'error': error,
        'data': data
    }


def return_error(ok=0, error='error', data=None):
    return {
        'success': 0,
        'ok': ok,
        'error': error,
        'data': data
    }
