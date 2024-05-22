import dao.category as dao


class Category(object):
    def __init__(self, category_id=None, dto=None):
        self.__id = dto.id if dto else None
        self.__name = dto.name if dto else None
        self.__description = dto.description if dto else None
        self.__folder = dto.folder if dto else None
        if category_id:
            self.__reload(category_id)

    def __reload(self, category_id: int):
        dto = dao.get(category_id)
        if dto:
            self.__id = dto.id
            self.__name = dto.name
            self.__description = dto.description
            self.__folder = dto.folder
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
    def folder(self):
        return self.__folder

    # STATICMETHODS #
    @staticmethod
    def all_categories():
        """Список всех категорий"""
        return dao.all_categories()

    # TODO написать dao метод
    # @staticmethod
    # def get_category_by_folder(category_folder=''):
    #     """Поиск категории по коду"""
    #     return dao.get_category_by_folder(category_folder=category_folder)
