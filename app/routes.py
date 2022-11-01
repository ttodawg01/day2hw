from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import SignUpForm, LogInForm, AddressForm
from app.models import User, Address


@app.route('/')
def index():
    addresses = Address.query.order_by(Address.date_created.desc()).all()
    return render_template('index.html', addresses=addresses)



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



@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = AddressForm()
    if form.validate_on_submit():
        #get data from the form
        address = form.address.data
        #create a new instance of address with the info from the form
        new_address = Address(address=address, user_id=current_user.id)
        #flash a message of success
        flash(f"{new_address} has been created", "success")
        #redirect back to the homepage
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


@app.route('/addresses/<address_id>')
def get_address(address_id):
    address = Address.query.get_or_404(address_id)
    if not address:
        flash(f"Address with {address_id} does not exist", "warning")
        return redirect(url_for('index'))
    return render_template('address.html', address=address)


@app.route('/addresses/<address_id>/edit', methods=['GET', 'POST'])
def edit_post(address_id):
    address = Address.query.get_or_404(address_id)
    if not address:
        flash(f"Address with {address_id} does not exist", "warning")
        return redirect(url_for('index'))
    if address.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))
    form = AddressForm()
    if form.validate_on_submit():
        #get the form data
        new_address = form.address.data
        #update the post
        address.update(address=new_address)
        flash(f"{address} has been updated", "success")
        return redirect(url_for('get_address', address_id=address.id))
    return render_template('edit_address.html', address=address, form=form)


@app.route('/addresses/<address_id>/delete')
@login_required
def delete_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"Address with {address_id} does not exist", "warning")
        return redirect(url_for('index'))
    if address.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('index'))
    address.delete()
    flash(f"{address} has been deleted", 'info')
    return redirect(url_for('index'))
