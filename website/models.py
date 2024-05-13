from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from wtforms import StringField, IntegerField, FileField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.fields.simple import HiddenField
from sqlalchemy import func, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

mail = Mail()
db = SQLAlchemy()
base = declarative_base()

class Agent(UserMixin, db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    properties = db.relationship('Property', backref='agent', lazy=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    square_meters = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(50), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=func.now())
    is_rented = db.Column(db.Boolean, nullable=False, default=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))  # Add foreign key
    tenant = relationship('Tenant', back_populates='rented_properties')  # Define relationship


class Tenant(UserMixin, db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    rented_properties = relationship('Property', back_populates='tenant', lazy=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    lease_period = db.Column(db.String(50), nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))  # Add agent_id column

    # Define relationship with Agent model
    agent = relationship('Agent', backref=db.backref('tenants', lazy=True))


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    name = db.Column(db.String(50), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=True)

class AddPropertyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    bathrooms = IntegerField('Bathrooms', validators=[DataRequired()])
    square_meters = IntegerField('Square Meters', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    agent_id = SelectField('Agent', validators=[DataRequired()])


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))  # Add agent_id column

    # Define relationship with Agent model
    agent = db.relationship('Agent', backref=db.backref('messages', lazy=True))




class InterestedUser(db.Model):
    __tablename__ = 'interested_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)  # New column for agent ID
    property = db.relationship('Property', backref=db.backref('interested_users', lazy=True))
    agent = db.relationship('Agent', backref=db.backref('interested_users', lazy=True))  # Relationship with Agent model

class InterestedUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message')
    property_id = HiddenField('Property ID')

class Leasing(db.Model):
    __tablename__ = 'leasings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    

class LeasingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    

class Selling(db.Model):
    __tablename__ = 'sellings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class SellingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])