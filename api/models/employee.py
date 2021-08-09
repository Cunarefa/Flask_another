from marshmallow import EXCLUDE, fields, validate
from marshmallow_sqlalchemy import auto_field
from sqlalchemy.ext.hybrid import hybrid_property

from api import db, ma

DATE_FORMAT = '%d-%m-%Y'


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    superior_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    superior = db.relationship('Employee', backref='employees', remote_side=[id], post_update=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def some(self):
        return self.employees[0]


class EmployeeSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    first_name = fields.String(validate=validate.Length(max=255))
    last_name = fields.String(validate=validate.Length(max=255))
    position = fields.String(validate=validate.Length(max=255))
    hire_date = fields.Date(format=DATE_FORMAT)
    salary = fields.Integer()
    superior_id = fields.Integer()
    employees = fields.List(fields.Nested(lambda: EmployeeSchema(exclude=("salary", "hire_date"))))


class UnEmployeeSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    first_name = fields.String(validate=validate.Length(max=255))
    last_name = fields.String(validate=validate.Length(max=255))
    position = fields.String(validate=validate.Length(max=255))
    hire_date = fields.Date(format=DATE_FORMAT)
    salary = fields.Integer()
    superior_id = fields.Integer()
