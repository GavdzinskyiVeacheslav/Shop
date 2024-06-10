import dao.order as dao
import model.models as model


class Order(object):
    def __init__(self, order_id=None, dto=None):
        self.__id = dto.id if dto else None
        self.__client_name = dto.client_name if dto else None
        self.__client_phone = dto.client_phone if dto else None
        self.__client_city = dto.client_city if dto else None
        self.__post_office = dto.post_office if dto else None
        self.__payment_method = dto.payment_method if dto else None
        self.__good_ids = dto.good_ids if dto else None
        self.__good_prices = dto.good_prices if dto else None
        self.__good_quantities = dto.good_quantities if dto else None
        if order_id:
            self.__reload(order_id)

    def __reload(self, order_id: int):
        dto = dao.get(order_id)
        if dto:
            self.__id = dto.id
            self.__client_name = dto.client_name
            self.__client_phone = dto.client_phone
            self.__client_city = dto.client_city
            self.__post_office = dto.post_office
            self.__payment_method = dto.payment_method
            self.__good_ids = dto.good_ids
            self.__good_prices = dto.good_prices
            self.__good_quantities = dto.good_quantities
        else:
            return None

    # PROPERTIES #
    @property
    def id(self):
        return self.__id

    @property
    def client_name(self):
        return self.__client_name

    @property
    def client_phone(self):
        return self.__client_phone

    @property
    def client_city(self):
        return self.__client_city

    @property
    def post_office(self):
        return self.__post_office

    @property
    def payment_method(self):
        return self.__payment_method

    @property
    def good_ids(self):
        return self.__good_ids

    @property
    def good_prices(self):
        return self.__good_prices

    @property
    def good_quantities(self):
        return self.__good_quantities

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
        dto.client_name = params.get('client_name', dto.client_name)
        dto.client_phone = params.get('client_phone', dto.client_phone)
        dto.client_city = params.get('client_city', dto.client_city)
        dto.post_office = params.get('post_office', dto.post_office)
        dto.payment_method = params.get('payment_method', dto.payment_method)
        dto.good_ids = params.get('good_ids', dto.good_ids)
        dto.good_prices = params.get('good_prices', dto.good_prices)
        dto.good_quantities = params.get('good_quantities', dto.good_quantities)
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
    def all_goods_ids():
        """Список всех айдишников заказов"""
        return dao.all_orders_ids()
