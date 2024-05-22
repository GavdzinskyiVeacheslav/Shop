import dao.section as dao


class Section(object):
    def __init__(self, section_id=None, dto=None):
        self.__id = dto.id if dto else None
        self.__name = dto.name if dto else None
        self.__category_id = dto.category_id if dto else None
        self.__description = dto.description if dto else None
        self.__folder = dto.folder if dto else None
        if section_id:
            self.__reload(section_id)

    def __reload(self, section_id: int):
        dto = dao.get(section_id)
        if dto:
            self.__id = dto.id
            self.__name = dto.name
            self.__category_id = dto.category_id
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
    def category_id(self):
        return self.__category_id

    @property
    def description(self):
        return self.__description

    @property
    def folder(self):
        return self.__folder

    # STATICMETHODS #
    @staticmethod
    def list_section_by_category(category_id=0):
        """Список разделов конкретной категории"""
        return [Section(dto=dto) for dto in dao.list_section_by_category(category_id=category_id)]

    # TODO написать dao метод
    # @staticmethod
    # def get_section_by_folder(section_folder=''):
    #     """Поиск раздела по коду"""
    #     return dao.get_section_by_folder(section_folder=section_folder)
