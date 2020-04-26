from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import setup_db, Employee, Entry
from form import *
from flask_wtf import Form


app = Flask(__name__)
db = setup_db(app)


@app.route('/')
def index():
    return redirect(url_for('login_form'))


@app.route('/login', methods=['GET'])
def login_form():
    form = LoginForm()
    return render_template('pages/login.html', form=form)


@app.route('/login', methods=['POST'])
def login_submission():
    form = LoginForm(request.form)
    if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
        flash('Username or Password is incorrect')
        return redirect(url_for('login_form'))
    app.config['PAYROLL_STATUS'] = True
    return redirect(url_for('home_page'))


@app.route('/logout')
def logout():
    app.config['PAYROLL_STATUS'] = False
    return redirect(url_for('login_form'))


@app.route('/home')
def home_page():
    if app.config['PAYROLL_STATUS'] == False:
        return redirect(url_for('login_form'))
    return render_template('pages/home.html')


@app.route('/show')
def show_employees():
    if app.config['PAYROLL_STATUS'] == False:
        return redirect(url_for('login_form'))
    data = []
    e_query = Employee.query.order_by('e_id').all()
    for e in e_query:
        ents = [i.info()
                for i in Entry.query.filter(Entry.e_id == e.e_id).all()]
        # print(ents[0])
        total_hours = sum([i['hours_worked'] for i in ents])
        balance = sum([i['allowences'] - i['deductions'] for i in ents])

        temp = {
            'e_id': e.e_id,
            'name': e.name,
            'h_r': e.hourly_rate,
            'total': total_hours,
            'balance': balance,
        }
        data.append(temp)

    return render_template('pages/show.html', employees=data)


@app.route('/create', methods=['GET'])
def create_form():
    if app.config['PAYROLL_STATUS'] == False:
        return redirect(url_for('login_form'))
    form = CreateForm()
    return render_template('pages/create.html', form=form)


@app.route('/create', methods=['POST'])
def create_form_submission():
    form = CreateForm(request.form)
    try:
        e_id = request.form['e_id']
        if Employee.query.get(e_id) is not None:
            flash('Employee with ' + str(e_id) + ' aready exists.')
        elif int(request.form['hourly_rate']) < 0:
            flash('Hourly Rate has to be greater than 0')
        else:
            name = request.form['name']
            hourly_rate = request.form['hourly_rate']
            new_employee = Employee(e_id, name, hourly_rate)
            Employee.insert(new_employee)
            flash('Employee ' + name + ' was successfully added!')
    except Exception as e:
        print(e)
    return redirect(url_for('create_form'))


@app.route('/add', methods=['GET'])
def add_content():
    if app.config['PAYROLL_STATUS'] == False:
        return redirect(url_for('login_form'))
    form = AddForm()
    return render_template('pages/add.html', form=form)


@app.route('/add', methods=['POST'])
def add_content_submission():
    form = AddForm(request.form)
    try:
        e_id = request.form['e_id']
        if Employee.query.get(e_id) is None:
            flash('There is no Employee with id ' + str(e_id))

        elif request.form['purpose'] == 'Add':
            month = request.form['month']
            year = request.form['year']
            if Entry.query.filter(Entry.e_id == e_id, Entry.month == month, Entry.year == year).one_or_none() is not None:
                flash('Entry for ' + month + '/' + str(year) +
                      ' alteady exists for emp' + str(e_id))
            else:
                hours_worked = request.form['hours_worked']
                deductions = request.form['deductions']
                allowences = request.form['allowences']
                en = Entry(e_id, year, month, hours_worked,
                           deductions, allowences)
                Entry.insert(en)
                flash('Entry edded successfully')

        elif request.form['purpose'] == 'Update':
            month = request.form['month']
            year = request.form['year']

            existing_ent = Entry.query.filter(
                Entry.e_id == e_id, Entry.month == month, Entry.year == year).one_or_none()
            if existing_ent is None:
                flash('There is not any entry for ' + month +
                      '/' + str(year) + ' under emp id' + str(e_id))
            else:
                existing_ent.hours_worked = request.form['hours_worked']
                existing_ent.deductions = request.form['deductions']
                existing_ent.allowences = request.form['allowences']
                Entry.update(existing_ent)
                flash('Entry Updated!!')

        elif request.form['purpose'] == 'Delete':
            month = request.form['month']
            year = request.form['year']
            ent = Entry.query.filter(
                Entry.e_id == e_id, Entry.month == month, Entry.year == year).one_or_none()
            if ent is None:
                flash('This Entry doesn\'t exist')
            else:
                Entry.delete(ent)
                flash('Entry deleted!!')
        return redirect(url_for('add_content'))
    except Exception as e:
        print(e)


@app.route('/payroll')
def payroll_page():
    if app.config['PAYROLL_STATUS'] == False:
        return redirect(url_for('login_form'))
    data = []
    e_query = Employee.query.order_by('e_id').all()
    for e in e_query:
        temp = {
            'e_id': e.e_id,
            'name': e.name
        }
        data.append(temp)

    return render_template('/pages/payroll.html', employees=data)


@app.route('/payroll/<e_id>', methods=['GET'])
def payroll_per_person(e_id):
    if app.config['PAYROLL_STATUS'] == False:
        return redirect(url_for('login_form'))
    person = Employee.query.get(e_id)

    all_entries = [i.info()
                   for i in Entry.query.filter(Entry.e_id == e_id).order_by('id').all()]

    register = [(i['month/year'], i['hours_worked'], i['deductions'], i['allowences'])
                for i in all_entries]

    data = {
        'e_id': person.e_id,
        'name': person.name,
        'hourly_rate': person.hourly_rate,
        'register': register,
    }

    total_hours = sum([i['hours_worked'] for i in all_entries])
    balance = sum([i['allowences'] - i['deductions'] for i in all_entries])

    total_salary = total_hours * data['hourly_rate'] + balance

    data['total_salary'] = total_salary

    return render_template('/pages/payroll_per_person.html', employee=data)
