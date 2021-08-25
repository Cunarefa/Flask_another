import os

import pytest
from faker.generator import random
from sqlalchemy.orm.session import close_all_sessions
from api import create_app, db
from api.models import Employee
from faker import Faker

fake = Faker()


@pytest.fixture
def client():
    _app = create_app()
    _app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
    client = _app.test_client()

    with _app.app_context():
        db.create_all()

        yield client

        close_all_sessions()
        db.drop_all()


lst_dict = [{'Director': 0}, {'Manager': 0}, {'Developer': 0}, {'HR': 0}, {'Some position': 0}]


def positions():
    position = lst_dict[0]
    for key in position:
        position[key] += 1
        if key == 'Director' and position[key] == 1:
            lst_dict.remove(position)
        elif key == 'Manager' and position[key] == 10:
            lst_dict.remove(position)
        elif key == 'Developer' and position[key] == 20:
            lst_dict.remove(position)
        elif key == 'HR' and position[key] == 30:
            lst_dict.remove(position)
        elif key == 'Some position' and position[key] == 40:
            lst_dict.remove(position)

        return key


@pytest.fixture
def fill_database():
    pos_id = {'Director': [], 'Manager': [], 'Developer': [], 'HR': [], 'Some position': []}
    for pk in range(1, 101):
        id = pk
        first_name = fake.first_name()
        last_name = fake.last_name()
        hire_date = fake.date()
        position = positions()

        pos_id[position].append(pk)

        if position == 'Director':
            salary = 20000
            superior_id = None
        elif position == 'Manager':
            salary = fake.random_int(13000, 15000, 500)
            superior_id = pos_id['Director'][0]
        elif position == 'Developer':
            salary = fake.random_int(8000, 11000, 500)
            superior_id = random.choice(pos_id['Manager'])
        elif position == 'HR':
            salary = fake.random_int(3500, 6500, 500)
            superior_id = random.choice(pos_id['Developer'])
        elif position == 'Some position':
            salary = fake.random_int(1000, 3000, 500)
            superior_id = random.choice(pos_id['HR'])

        employee = Employee(id=id, first_name=first_name, last_name=last_name, hire_date=hire_date, position=position,
                            salary=salary, superior_id=superior_id)
        db.session.add(employee)
        db.session.commit()
