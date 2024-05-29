import os
from PIL import Image
from utils.config import get_config


def get_picture_sizes(item_id=0):
    """Получить размеры картинок"""
    picture_file = picture_path(item_id=item_id)
    image = Image.open(picture_file)
    width, height = image.size
    return width, height


# Удаление картинок - пока что не используется

# def delete_pictures(item_id=0):
#     """Удаление картинок"""
#     for preview in (False, True):
#         if os.path.isfile(picture_path(item_id=item_id)):
#             os.remove(picture_path(item_id=item_id))


def root_path(item_id=0, preview=False):
    """Корневой путь"""

    goods_images_path = get_config()['general'].get('goods_images_path', '')

    if preview:
        folder = os.path.join(goods_images_path, 'static', 'preview', str(int(item_id / 1000) + 1))
    else:
        folder = os.path.join(goods_images_path, 'static', 'pictures', str(int(item_id / 1000) + 1))

    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def picture_path(item_id=0):
    """Собрать путь к картинке"""
    return os.path.join(root_path(item_id=item_id), str(item_id) + '.jpg')


def picture_url(item_id=0, preview=False):
    """Вернуть адрес картинки начиная от папки"""
    if preview:
        return 'preview/' + str(int(item_id / 1000) + 1) + '/' + \
               str(item_id) + '.jpg'
    else:
        return 'pictures/' + str(int(item_id / 1000) + 1) + '/' + str(item_id) + '.jpg'
