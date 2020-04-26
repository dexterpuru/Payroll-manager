from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length
from models import Employee

months = [
    ('JAN', 'JAN'),
    ('FEB', 'FEB'),
    ('MAR', 'MAR'),
    ('APR', 'APR'),
    ('MAY', 'MAY'),
    ('JUN', 'JUN'),
    ('JUL', 'JUL'),
    ('AUG', 'AUG'),
    ('SEP', 'SEP'),
    ('OCT', 'OCT'),
    ('NOV', 'NOV'),
    ('DEC', 'DEC'),
]

max_year = 2025

years = [(str(i), str(i)) for i in range(2020, max_year+1)]

purposes = [
    ('Add', 'Add'),
    ('Update', 'Update'),
    ('Delete', 'Delete'),
]


class CreateForm(Form):
    e_id = IntegerField(
        'e_id', validators=[DataRequired()]
    )
    name = StringField(
        'name', validators=[DataRequired(), Length(max=100)]
    )
    hourly_rate = IntegerField(
        'hourly_rate', validators=[DataRequired()]
    )


class AddForm(Form):
    purpose = SelectField(
        'purpose', validators=[DataRequired()],
        choices=purposes
    )
    e_id = IntegerField(
        'e_id', validators=[DataRequired()]
    )
    hours_worked = IntegerField(
        'hours_worked', validators=[DataRequired()], default=0
    )
    month = SelectField(
        'month', validate_choice=False,
        choices=months
    )
    year = SelectField(
        'year', validate_choice=False,
        choices=years
    )
    deductions = IntegerField(
        'deductions', validators=[DataRequired()], default=0
    )
    allowences = IntegerField(
        'allowences', validators=[DataRequired()], default=0
    )


class LoginForm(Form):
    username = StringField(
        'username', validators=[DataRequired()]
    )
    password = StringField(
        'password', validators=[DataRequired()]
    )
