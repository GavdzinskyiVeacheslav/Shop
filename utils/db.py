from utils import log
import mysql.connector
from utils.config import get_config


def db_connection_settings():
    """Получение из конфига настроек разового подключения к БД"""
    db_config = get_config()
    p = db_config['db']
    connection_settings = {
        'user': p.get('user'),
        'password': p.get('password'),
        'host': p.get('host'),
        'database': p.get('database'),
    }
    return connection_settings


def db_connection():
    config = db_connection_settings()
    return mysql.connector.connect(**config)


# Подключение ко второй базе если нужно
# def db_connection_shop():
#     return mysql.connector.connect(
#         user='Slava',
#         password='Nub4ek114455',
#         host='localhost',
#         database='shop',
#     )


def db_statement(statement_type, sql, params, dictionary=True, auto_commit=True, db_connection_param=None):
    """
    Запуск исполняемого оператора MySQL

    Параметры:
    - statement_type: str       - тип оператора Row/List/Execute
    - sql: str                  - код запроса
    - params: Tuple             - подключаемые параметры
    - dictionary: boolean       - возвращает словарь/кортеж, необязательный

    Возвращает:
    - statement_type Row:       - Dictionary
    - statement_type List:      - List of Dictionary
    - statement_type Execute:   - int: ID добавленной/изменённой записи
    """
    connection = db_connection_param if db_connection_param else None
    cursor = None
    try:
        if db_connection_param is None:
            config = db_connection_settings()
            connection = mysql.connector.connect(**config)

        cursor = connection.cursor(dictionary=True if dictionary else False)
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute(sql, params)

        return_result = None
        if statement_type == 'Execute':
            return_result = cursor.rowcount
        elif statement_type == 'Insert':
            return_result = cursor.lastrowid
        elif statement_type == 'Row':
            return_result = cursor.fetchone()
        elif statement_type == 'List':
            return_result = cursor.fetchall()
        else:
            log.write('Wrong database operation type')
        if auto_commit:
            connection.commit()
        return return_result

    except Exception as error:
        if connection:
            connection.rollback()
        log.write('Database connection error: ' + str(error))
        raise error
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected() and auto_commit:
            connection.close()
