import inspect
import logging
import os
import datetime
import traceback

if not os.path.exists(os.getcwd() + '/logs'):
    os.mkdir(os.getcwd() + '/logs')

""" Логи пишутся в систему в кодировке ANSI по умолчанию
    Если в лог будет писаться не локальный язык машины, то лог будет падать с ошибками.
    Пишем в файл с кодировкой utf-8 """

# Повышение уровня c DEBUG на WARNING логгера конкретно библиотеки Pillow
logger_pillow = logging.getLogger('PIL')
logger_pillow.setLevel(logging.WARNING)

logging.basicConfig(
    handlers=[
        logging.FileHandler(
            filename=f"{os.getcwd()}/logs/{datetime.date.isoformat(datetime.date.today())}.log",
            mode='a',
            encoding='utf-8'
        )
    ],
    format='%(asctime)s %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.DEBUG,
)


def write(message, level='error'):
    if level.lower() not in ['debug', 'error', 'warning', 'info', 'critical', 'fiction']:
        level = 'error'
    try:
        if level != 'fiction':  # fiction нужен для "пустого" обработчика ошибки
            logger = logging.getLogger(find_caller())
            logger.setLevel(getattr(logging, level.upper()))  # Значение переменной по модулю и имени
            getattr(logger, level.lower())(message)  # Вызов метода по объекту и имени
    except Exception as e:
        print('logger.' + level.lower() + ' unexpected exception ' + str(e))


def find_caller():
    try:
        stack_summary = traceback.StackSummary.extract(traceback.walk_stack(None))
        print(stack_summary)
        if stack_summary and len(stack_summary) > 1:
            return (stack_summary[2].filename + ' line ' + str(stack_summary[2].lineno)
                    + ' function ' + stack_summary[2].name)
    except Exception as e:
        print('logger.find_caller unexpected exception ' + str(e))
    return 'unknown'


def debug_line():
    caller_frame_record = inspect.stack()[1]  # 0 represents this line
    # 1 represents line at caller
    frame = caller_frame_record[0]
    info = inspect.getframeinfo(frame)
    write(f"{info.filename} - {info.function} - {info.lineno}")
