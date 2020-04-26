from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    migrate = Migrate(app, db)
    return db


class Employee(db.Model):
    __tablename__ = 'employees'

    e_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    hourly_rate = db.Column(db.Integer, nullable=False)

    def __init__(self, e_id, name, hourly_rate):
        self.e_id = e_id
        self.name = name
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return f'<Employee {self.e_id}, name:{self.name}, hourly_rate: {self.hourly_rate}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short_info(self):
        return {
            'id': self.e_id,
            'name': self.name,
            'hourly_rate': self.hourly_rate
        }


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    # cur_salary
    e_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(), nullable=False)
    hours_worked = db.Column(db.Integer, nullable=False)
    deductions = db.Column(db.Integer, nullable=False)
    allowences = db.Column(db.Integer, nullable=False)

    def __init__(self, e_id, year, month, hours_worked=0, deductions=0, allowences=0):
        self.e_id = e_id
        self.year = year
        self.month = month
        self.hours_worked = hours_worked
        self.deductions = deductions
        self.allowences = allowences

    def __repr__(self):
        return f'<Entry: {self.id}, Emp_id: {self.e_id}, month/year: {self.month}/{self.year}, hours_worked: {self.hours_worked}, deductions: {self.deductions}, allowences: {self.allowences}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def info(self):
        return {
            'id': self.id,
            'e_id': self.e_id,
            'month/year': [self.month, self.year],
            'hours_worked': self.hours_worked,
            'deductions': self.deductions,
            'allowences': self.allowences
        }
