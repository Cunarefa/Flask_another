"""empty_rev

Revision ID: 31db6c32caf6
Revises: d43b96d76067
Create Date: 2021-07-26 15:40:48.357346

"""

from alembic import op
import sqlalchemy as sa
from faker import Faker
from faker.generator import random
from sqlalchemy import table
from sqlalchemy.sql.elements import Null

from api.models.employee import DATE_FORMAT

fake = Faker()

# revision identifiers, used by Alembic.
revision = '31db6c32caf6'
down_revision = 'd43b96d76067'
branch_labels = None
depends_on = None


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


def data():
    lst = []
    pos_id = {'Director': [], 'Manager': [], 'Developer': [], 'HR': [], 'Some position': []}
    for pk in range(1, 101):
        fake_data = dict()

        fake_data["id"] = pk
        fake_data["first_name"] = fake.first_name()
        fake_data["last_name"] = fake.last_name()
        fake_data["position"] = positions()
        fake_data["hire_date"] = fake.date()

        pos_id[fake_data["position"]].append(pk)

        if fake_data["position"] == 'Director':
            fake_data["salary"] = 20000
            fake_data["superior_id"] = None
        elif fake_data["position"] == 'Manager':
            fake_data["salary"] = fake.random_int(13000, 15000, 500)
            fake_data["superior_id"] = pos_id['Director'][0]
        elif fake_data["position"] == 'Developer':
            fake_data["salary"] = fake.random_int(8000, 11000, 500)
            fake_data["superior_id"] = random.choice(pos_id['Manager'])
        elif fake_data["position"] == 'HR':
            fake_data["salary"] = fake.random_int(3500, 6500, 500)
            fake_data["superior_id"] = random.choice(pos_id['Developer'])
        elif fake_data["position"] == 'Some position':
            fake_data["salary"] = fake.random_int(1000, 3000, 500)
            fake_data["superior_id"] = random.choice(pos_id['HR'])

        lst.append(fake_data)

    return lst


def upgrade():
    employees = table('employees',
                      sa.Column('id', sa.Integer(), nullable=False),
                      sa.Column('first_name', sa.String(length=255), nullable=False),
                      sa.Column('last_name', sa.String(length=255), nullable=False),
                      sa.Column('position', sa.String(length=255), nullable=False),
                      sa.Column('hire_date', sa.Date(), nullable=False),
                      sa.Column('salary', sa.Integer(), nullable=False),
                      sa.Column('superior_id', sa.Integer(), nullable=True)
                      )

    op.bulk_insert(employees, data())


def downgrade():
    pass

