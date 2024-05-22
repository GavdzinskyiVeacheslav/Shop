import decimal

import re

from flask import render_template

from business.category import Category
from business.section import Section


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


def parse_int(value: any = None) -> int:
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


def match_format_and(text):
    """Формат для поиска ('беннет     либерман нетанияху ' -> '+беннет* +либерман* +нетанияху*')"""
    return ' '.join([f'+{word}*' for word in text.strip().split(' ') if word])


def process_param(param_name: str, params: dict, default='', is_numeric=False):
    """cut_inject и parse_int в одной функции"""
    value = params.get(param_name, default)
    cleaned_value = cut_inject(text=str(value)).strip()
    return parse_int(cleaned_value) if is_numeric else cleaned_value


def categories_sections_list():
    """Списки категорий и разделов"""

    categories = Category.all_categories()
    sections = {}
    for category in categories:
        sections[category.id] = Section.list_section_by_category(category_id=category.id)

    return categories, sections


def remove_html_tags_and_links(text=''):
    """Убирает html тэги и ссылки"""
    # Pattern to match HTML tags
    tag_re = re.compile(r'<[^>]+>')
    # Pattern to match URLs
    url_re = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # Remove HTML tags
    result = tag_re.sub('', text)
    # Remove URLs
    result = url_re.sub('', result)

    return result
