
# from re import L
from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import SignUpForm


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/form', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted')

        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)

        #flash a success message
        flash('You have successfully signed up')

        return redirect(url_for('index'))
    return render_template('form.html', form=form)