from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from flask_login import current_user, login_required
from .models import db, Agent, Property, Tenant, Admin, Message, InterestedUser, Leasing, Selling, InterestedUserForm, SellingForm, LeasingForm
from flask_mail import Mail

mail = Mail()
routes = Blueprint('routes', __name__)

@routes.route('/') 
def index():
    return render_template('index.html')

@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/contact')
def contact():
    return render_template('contact.html')

@routes.route('/admin')
@login_required
def admin():
    tenants = Tenant.query.all()
    agents = Agent.query.all()
    properties = Property.query.all()
    messages = Message.query.all()  

    return render_template('admin.html', tenants=tenants, agents=agents, properties=properties, messages=messages)

@routes.route('/agent')
@login_required
def agent():
    leased_properties = Property.query.filter_by(agent_id=current_user.id, is_rented=True).all()
    unleased_properties = Property.query.filter_by(agent_id=current_user.id, is_rented=False).all()

    interested_users = InterestedUser.query.filter_by(agent_id=current_user.id).all()
    tenants = Tenant.query.filter_by(agent_id=current_user.id).all()
    messages = Message.query.filter_by(agent_id=current_user.id).all()

    return render_template('agent.html', leased_properties=leased_properties, 
                           interested_users=interested_users, 
                           tenants=tenants, messages=messages, unleased_properties = unleased_properties)

                           
@routes.route('/leasing', methods=['GET', 'POST'])
def leasing():
    form = LeasingForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # Create instance of Selling model and save to the database
        selling_entry = Selling(name=name, email=email, message=message)
        db.session.add(leasing_entry)
        db.session.commit()
        
        # Send email notification
        msg = Message(
            subject='Leasing Inquiry from ' + name,
            sender=email,
            recipients=['your-email@example.com'],  # Replace with your email
            body=message
        )
        mail.send(msg)
        
        flash('Your inquiry has been sent successfully.', 'success')
        return redirect(url_for('routes.leasing'))
    
    return render_template('leasing.html', form=form)


@routes.route('/selling', methods=['GET', 'POST'])
def selling():
    form = SellingForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # Create instance of Selling model and save to the database
        selling_entry = Selling(name=name, email=email, message=message)
        db.session.add(selling_entry)
        db.session.commit()
        
        # Send email notification
        msg = Message(
            subject='Selling Inquiry from ' + name,
            sender=email,
            recipients=['your-email@example.com'],  # Replace with your email
            body=message
        )
        mail.send(msg)
        
        flash('Your inquiry has been sent successfully.', 'success')
        return redirect(url_for('routes.selling'))
    
    return render_template('selling.html', form=form)



@routes.route('/property_interest/<int:property_id>/', methods=['GET', 'POST'])
def property_interest(property_id):
    form = InterestedUserForm()
    property = Property.query.get_or_404(property_id)
    if form.validate_on_submit():
        agent = property.agent
        subject = f'Interest in {property.name} from {form.name.data}'
        sender = form.email.data
        body = f'{form.name.data} ({form.email.data}) has expressed interest in your property "{property.name}".'
        recipients = [agent.email]
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        mail.send(msg)

        flash('Your interest in the property has been recorded.', 'success')
        return redirect(url_for('routes.property_interest', property_id=property_id))
    return render_template('property_interest.html', form=form, property=property)



@routes.route('/property')
def property():
    properties = Property.query.all()
    return render_template('property.html', properties=properties)

@routes.route('/tenant')
@login_required  # Ensure the user is logged in as a tenant
def tenant():
    # Filter properties and agent associated with the logged-in tenant
    tenant = Tenant.query.get(current_user.id)
    rented_properties = tenant.rented_properties
    agent = tenant.agent

    return render_template('tenant.html', rented_properties=rented_properties, agent=agent)
