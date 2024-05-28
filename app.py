from flask import Flask

from public.routes import public_bp
from control.routes import control_bp
from utils.config import get_config

# Инициализация приложения
app = Flask(
    __name__,
)

# Регистрация Блюпринта
app.register_blueprint(public_bp, url_prefix='/')
app.register_blueprint(control_bp, url_prefix='/control')
# Secret key
app.secret_key = get_config()['secret_key'].get('key', "")

if __name__ == '__main__':
    app.run(
        debug=True,
        use_reloader=False,
        port=get_config()['general'].get('port', 5100)
    )
