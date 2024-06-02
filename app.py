from datetime import datetime

from flask import Flask

from public.routes import public_bp
from control.routes import control_bp
from utils.common import categories_sections_list
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


@app.context_processor
def template_context():
    """Процессор контекста для всего приложения"""

    # Категории и разделы
    categories, sections = categories_sections_list()

    return dict(
        current_year=datetime.now().year,
        categories=categories,
        sections=sections,
    )


if __name__ == '__main__':
    app.run(
        debug=True,
        use_reloader=False,
        port=get_config()['general'].get('port', 5100)
    )
