import dao.photo as dao
import model.models as model
from utils import picture_utils


class Photo(object):
    def __init__(self, photo_id=None, dto=None):
        self.__id = dto.id if dto else None
        self.__good_id = dto.good_id if dto else None
        self.__width = dto.width if dto else None
        self.__height = dto.height if dto else None
        if photo_id:
            self.__reload(photo_id)

    def __reload(self, photo_id: int):
        dto = dao.get(photo_id)
        if dto:
            self.__id = dto.id
            self.__good_id = dto.good_id
            self.__width = dto.width
            self.__height = dto.height

        else:
            return None

    # PROPERTIES #
    @property
    def id(self):
        return self.__id

    @property
    def good_id(self):
        return self.__good_id

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def picture(self):
        return picture_utils.picture_url(item_id=self.__id)

        # CRUD #

    def insert(self, **params):
        """Добавление записи в БД"""
        dto = model.Photo(**params)
        new_id = dao.create(dto)
        dto.id = new_id
        self.__reload(new_id)
        return new_id

    def update(self, **params):
        """Изменение записи в БД"""
        dto = dao.get(self.__id)
        if dto is None:
            return None
        dto.good_id = params.get('good_id', dto.good_id)
        dto.width = params.get('width', dto.width)
        dto.height = params.get('height', dto.height)

        dao.update(
            photo=dto,
        )
        self.__reload(self.__id)

    @staticmethod
    def delete(photo_id):
        """Удаление записи из БД"""
        dto = dao.get(photo_id)
        if dto is None:
            return None
        deleted = dao.delete(
            photo_id,
        )
        return True if deleted else False

    # STATICMETHODS #
    @staticmethod
    def all_photo_items_by_good(good_id=0):
        """Список объектов всех фотографий конкретного товара"""
        return [Photo(dto=dto) for dto in dao.all_photo_items_by_good(good_id=good_id)]
