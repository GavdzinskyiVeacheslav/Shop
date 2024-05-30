from functools import wraps

from flask import session, redirect, url_for, request, render_template, flash

from control.routes import control_bp
from utils.config import get_config


def check_logged_in():
    """Декоратор контроллеров для проверки наличия авторизации сотрудника"""
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # На логин
            if 'admin' not in session:
                return redirect(url_for('control.login'))

            # Аутентификация успешна прошла
            if 'admin' in session:
                return func(*args, **kwargs)

        return wrapper
    return actual_decorator


@control_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Форма логина"""
    if request.method == 'POST':
        # Проверяем имя
        if request.form.get('employee_name', '') == get_config()['auth'].get('name', ''):
            # Проверяем пароль
            if request.form.get('password', '') == get_config()['auth'].get('password', ''):
                # Записываем в flask-сессию
                session['admin'] = 'admin'
            # Неправильный пароль
            else:
                flash('Неправильный пароль', 'error')
        # Неправильное имя
        else:
            flash('Неправильное имя', 'error')

        # Всё совпало - продолжаем программу и редирект в защищённую зону
        return redirect(url_for('control.add_photo'))

    # GET
    return render_template(
        '/control/login.html',
    )


@control_bp.route('/logout')
def logout():
    """Выход из системы"""
    # Убрать из сессии
    session.pop('admin', None)
    # Редирект на логин
    return redirect(url_for('control.login'))
