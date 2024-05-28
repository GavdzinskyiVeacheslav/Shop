from flask import Blueprint

control_bp = Blueprint(
    'control',
    __name__,
    template_folder='templates',
    static_folder='static',
)

