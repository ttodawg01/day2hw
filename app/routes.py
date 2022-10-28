from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import SignUpForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/form', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted')
        # print(form.errors)

        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)

        #creating a new user
        new_user = User(first_name=first_name, last_name=last_name,
        phone_number=phone_number, address=address)

        #flash a success message
        flash(f'{new_user} have successfully signed up!')

        return redirect(url_for('index'))
    return render_template('form.html', form=form)