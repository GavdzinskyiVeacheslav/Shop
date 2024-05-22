import dao.order as dao
import model.models as model


class Order(object):
    def __init__(self, order_id=None, dto=None):
        self.__id = dto.id if dto else None
        self.__name = dto.name if dto else None
        self.__description = dto.description if dto else None
        if order_id:
            self.__reload(order_id=order_id)

    def __reload(self, order_id: int):
        dto = dao.get(order_id=order_id)
        if dto:
            self.__id = dto.id
            self.__name = dto.name
            self.__description = dto.description
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

    # CRUD #
    def insert(self, **params):
        """Добавление записи в БД"""
        dto = model.Order(**params)
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
        dao.update(
            order=dto,
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
    def all_orders_ids():
        """Список всех айдишников заказов"""
        return dao.all_orders_ids()
