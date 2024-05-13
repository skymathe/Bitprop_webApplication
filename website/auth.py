from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Agent, Admin, Tenant, Property
from .models import  AddPropertyForm, db


auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = Tenant.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already exists. Please log in.', category= 'danger')
            return redirect(url_for('auth.login'))

        new_user = Tenant(name=name, email=email, password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. Please log in.', category= 'success')
        login_user(new_user)
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Agent.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash('Login successful.', category='success')
            login_user(user) 
            return redirect(url_for('routes.agent'))

        user = Admin.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash('Login successful.', category= 'success')
            login_user(user) 
            return redirect(url_for('routes.admin'))

        user = Tenant.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash('Login successful.', category='success')
            login_user(user) 
            return redirect(url_for('routes.tenant'))

        flash('Login unsuccessful. Please check your email and password.', category= 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@auth.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    """
    Add a new property
    """
    if not isinstance(current_user, Admin):
        flash('Access denied')
        return redirect(url_for('index'))  # Assuming 'index' is the correct route

    form = AddPropertyForm()

    if form.validate_on_submit():
        # Extract form data into separate variables for better readability
        name = form.name.data
        description = form.description.data  # Fixed: Use 'description' instead of 'name'
        address = form.address.data
        price = form.price.data
        bedrooms = form.bedrooms.data
        bathrooms = form.bathrooms.data
        square_meters = form.square_meters.data
        image = form.image.data
        agent_id = form.agent_id.data

        # Create a new Property instance
        property = Property(
            name=name,
            description=description,
            address=address,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            square_meters=square_meters,
            image=image.filename,
            agent_id=agent_id
        )

        # Add the new property to the database session and commit
        db.session.add(property)
        db.session.commit()

        flash('Property added')
        return redirect(url_for('auth.admin'))

    # Only render the template once, with the form and agents passed as context variables
    return render_template('add_property.html', form=form, agents=Agent.query.all())
