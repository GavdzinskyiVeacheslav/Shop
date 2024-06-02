import dao.good as dao
import model.models as model
from business.category import Category
from business.section import Section


# Константы
START_CUTTING = 0
END_CUTTING = 100


class Good(object):
    def __init__(self, good_id=None, dto=None):
        self.__id = dto.id if dto else None
        self.__name = dto.name if dto else None
        self.__description = dto.description if dto else None
        self.__category_id = dto.category_id if dto else None
        self.__section_id = dto.section_id if dto else None
        self.__price = dto.price if dto else None
        self.__existence = dto.existence if dto else None
        self.__add_date = dto.add_date if dto else None
        self.__picture = None
        self.__section = None
        self.__category = None
        if good_id:
            self.__reload(good_id)

    def __reload(self, good_id: int):
        dto = dao.get(good_id)
        if dto:
            self.__id = dto.id
            self.__name = dto.name
            self.__description = dto.description
            self.__category_id = dto.category_id
            self.__section_id = dto.section_id
            self.__price = dto.price
            self.__existence = dto.existence
            self.__add_date = dto.add_date

        else:
            return None

    # PROPERTIES #
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def short_description(self):
        return self.__description[START_CUTTING:END_CUTTING]

    @property
    def category_id(self):
        return self.__category_id

    @property
    def section_id(self):
        return self.__section_id

    @property
    def price(self):
        return self.__price

    @property
    def existence(self):
        return self.__existence

    @property
    def add_date(self):
        return self.__add_date

    @property
    def section(self):
        return Section(section_id=self.__section_id) if not self.__section else self.__section

    @property
    def category(self):
        return Category(category_id=self.section.category_id) if not self.__category else self.__category

    # CRUD #

    def insert(self, **params):
        """Добавление записи в БД"""
        dto = model.Good(**params)
        new_id = dao.create(dto)
        dto.id = new_id
        self.__reload(new_id)
        return True

    def update(self, **params):
        """Изменение записи в БД"""
        dto = dao.get(self.__id)
        if dto is None:
            return None
        dto.name = params.get('name', dto.name)
        dto.description = params.get('description', dto.description)
        dto.category_id = params.get('category_id', dto.category_id)
        dto.section_id = params.get('section_id', dto.section_id)
        dto.add_date = params.get('add_date', dto.add_date)
        dto.price = params.get('price', dto.price)
        dto.existence = params.get('existence', dto.existence)

        dao.update(
            good=dto,
        )
        self.__reload(self.__id)

    @staticmethod
    def delete(order_id):
        """Удаление записи из БД"""
        dto = dao.get(order_id)
        if dto is None:
            return None
        deleted = dao.delete(
            order_id,
        )
        return True if deleted else False

    # STATICMETHODS #
    @staticmethod
    def all_goods_ids():
        """Список всех айдишников товаров"""
        return dao.all_goods_ids()

    @staticmethod
    def good_ids_by_search(search=''):
        """Список айдишников товаров по поиску"""
        return dao.good_ids_by_search(search=search)
