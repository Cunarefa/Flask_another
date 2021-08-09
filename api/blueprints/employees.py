from flask import request, abort, jsonify
from marshmallow import ValidationError
from sqlalchemy import text

from api import db
from api.blueprints import emp_api
from api.models.employee import EmployeeSchema, Employee, UnEmployeeSchema


@emp_api.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = db.session.query(Employee).filter(Employee.id == employee_id).first_or_404()

    schema = EmployeeSchema()
    return schema.dump(employee), 200


@emp_api.route('/employees', methods=['POST'])
def add_employee():
    json_data = request.json

    schema = EmployeeSchema()
    try:
        data = schema.load(json_data)
    except ValidationError:
        return abort(400, description="Invalid data type of some fields.")

    employee = Employee(**data)

    db.session.add(employee)
    db.session.commit()
    return schema.dump(employee), 201


@emp_api.route('/employees/<int:employee_id>', methods=['PATCH'])
def update_employee(employee_id):
    employee = db.session.query(Employee).filter(Employee.id == employee_id).first_or_404()

    schema = EmployeeSchema()
    json_data = request.json

    try:
        data = schema.load(json_data)
    except ValidationError as err:
        return abort(400, description=err)

    db.session.query(Employee).filter(Employee.id == employee_id).update(data)
    db.session.add(employee)
    db.session.commit()
    return schema.dump(employee)


def nested_employees_quantity(employee, emp_quantity):
    if len(employee.employees) == 0:
        return employee
    for emp in employee.employees[0:emp_quantity]:
        nested_employees_quantity(emp, emp_quantity)

        employee.employees = employee.employees[0:emp_quantity]
    return employee


@emp_api.route('/employees', methods=['GET'])
def get_employees():
    employee = Employee.query.get(1)

    emp_quantity = request.args.get("emp_quantity")
    if emp_quantity:
        employee = nested_employees_quantity(employee, int(emp_quantity))

    schema = EmployeeSchema()
    return schema.dump(employee)


@emp_api.route('/employees/all', methods=['GET'])
def get_all_employees():
    employees = db.session.query(Employee)

    page = request.args.get("page", 1, type=int)

    position = request.args.get("position")
    salary = request.args.get("salary")
    min_salary = request.args.get("min_salary")
    max_salary = request.args.get("max_salary")
    order_by = request.args.get("order_by")
    ordering = request.args.get("ordering")

    if position:
        employees = employees.filter(Employee.position == position)
    if salary:
        employees = employees.filter(Employee.salary == salary)
    if min_salary and max_salary:
        employees = employees.filter((min_salary < Employee.salary) & (Employee.salary < max_salary))
    if order_by and ordering:
        employees = employees.order_by(text(f'{order_by} {ordering}'))
    if page:
        employees = employees.paginate(page, 10, False).items

    schema = UnEmployeeSchema(many=True)
    return jsonify(schema.dump(employees))




