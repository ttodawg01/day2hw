from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import app
from app.forms import SignUpForm, LogInForm
from app.models import User


@app.route('/')
def index():
    print(current_user)
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
        #check to see if we have the same information submitted again
        check_user = User.query.filter( (User.first_name == first_name) | (User.address == address) ).first()
        if check_user is not None:
            flash("User with First Name/Address already exists", "danger")
            return redirect(url_for('index'))

        #creating a new user
        new_user = User(first_name=first_name, last_name=last_name,
        phone_number=phone_number, address=address)

        #flash a success message
        flash(f'{new_user} have successfully signed up!')

        return redirect(url_for('index'))
    return render_template('form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        # get the form data
        first_name = form.first_name.data
        address = form.address.data
        #check to see if their is another user with the same first name and address
        user = User.query.filter_by(first_name=first_name).first()
        # user2 = User.query.filter_by(address=address).first()
        if user is not None:
            #log the user in 
            login_user(user)
            flash(f"{user} is now logged in", "primary")
            return redirect(url_for('index'))
        else:
            flash("Incorrect First name and/or Address. Please try again", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))