from flask import Blueprint

emp_api = Blueprint('emp_api', __name__)

from api.blueprints import employees
