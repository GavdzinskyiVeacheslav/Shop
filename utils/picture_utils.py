import os
from PIL import Image

from utils.config import get_config

PICTURE_WIDTH = 300
PICTURE_HEIGHT = 300

PREVIEW_WIDTH = 150
PREVIEW_HEIGHT = 150


def get_picture_sizes(item_id=0):
    """Получить размеры картинок"""
    picture_file = picture_path(item_id=item_id)
    image = Image.open(picture_file)
    width, height = image.size
    return width, height


def save_preview(item_id=0):
    """Сохранение"""
    picture_file = picture_path(item_id=item_id)
    image = Image.open(picture_file)

    # Уменьшить пропорционально для preview
    width, height = image.size

    # Горизонтальная
    if width <= height:
        preview_width = PREVIEW_WIDTH
        preview_height = int(height * preview_width / width)

    # Вертикальная
    else:
        preview_height = PREVIEW_HEIGHT
        preview_width = int(width * preview_height / height)

    resized = image.resize((preview_width, preview_height))
    return resized.save(os.path.join(root_path(item_id=item_id, preview=True), str(item_id) + '.png'))


def delete_pictures(item_id=0):
    """Удаление картинок"""
    for preview in (False, True):
        if os.path.isfile(picture_path(item_id=item_id, preview=preview)):
            os.remove(picture_path(item_id=item_id, preview=preview))


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


def picture_path(item_id=0, preview=False):
    """Собрать путь к картинке"""
    return os.path.join(root_path(item_id=item_id, preview=preview), str(item_id) + '.png')


def picture_url(item_id=0, preview=False):
    """Вернуть адрес картинки начиная от папки"""
    if preview:
        return 'preview/' + str(int(item_id / 1000) + 1) + '/' + \
               str(item_id) + '.jpg'
    else:
        return 'pictures/' + str(int(item_id / 1000) + 1) + '/' + str(item_id) + '.png'
