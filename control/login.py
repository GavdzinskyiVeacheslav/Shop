from functools import wraps

from flask import session, redirect, url_for, request, render_template

from control.routes import control_bp


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
    if request.method == 'POST':
        if request.form.get('employee_name', '') == 'Вася':
            if request.form.get('password', '') == '123':
                session['admin'] = 'admin'

        return redirect(url_for('control.add_photo'))

    return render_template(
        '/control/login.html',
    )
