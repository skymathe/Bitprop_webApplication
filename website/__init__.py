# -*- coding: utf-8 -*-
import random
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from .models import Property, db

DB_NAME = "database.db"

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = '7ca8ed167aad8f'
    MAIL_PASSWORD = '2477a587104dd7'
    ADMINS = ['your-email@example.com']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail = Mail(app)  # Initialize the mail instance

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth,  url_prefix='/')

    from .models import AddPropertyForm, Admin, Agent, Property, Tenant

    create_database(app)
    create_users(app)
    create_random_houses(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = Admin.query.get(int(id))
        if user:
            return user
        user = Agent.query.get(int(id))
        if user:
            return user
        user = Tenant.query.get(int(id))
        return user 
    
    return app

def create_database(app):
    with app.app_context():
        db.create_all()

def create_users(app):
    """Create users if they don't already exist."""
    with app.app_context():
        from .models import Admin, Agent, Tenant

        # Define users including the admin
        users = [
            ('Admin', 'your-email@example.com', 'admin-password', True),
            ('Agent 1', 'agent1@example.com', 'agent-password', False),
            ('Agent 2', 'agent2@example.com', 'agent-password', False),
            ('Tenant 1', 'tenant1@example.com', 'tenant-password', False),
            ('Tenant 2', 'tenant2@example.com', 'tenant-password', False),
            ('Tenant 3', 'tenant3@example.com', 'tenant-password', False),
            ('Tenant 4', 'tenant4@example.com', 'tenant-password', False),
        ]

        for name, email, password, is_admin in users:
            user_class = Admin if is_admin else Agent if 'Agent' in name else Tenant
            user = user_class.query.filter_by(email=email).first()
            if not user:
                user = user_class(
                    name=name,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=is_admin
                )
                db.session.add(user)

        db.session.commit()
        print("Created users!")


def generate_random_house(app):
    """Generate a random house with random values for each attribute."""
    with app.app_context():
        name = f"Random House {random.randint(1, 1000)}"
        description = f"This is a random house with a random description."
        address = f"Random Street {random.randint(1, 1000)}"
        price = round(random.uniform(1000, 5000), 2)
        bedrooms = random.randint(2, 5)
        bathrooms = random.randint(1, 3)
        square_meters = round(random.uniform(50, 500), 2)
        image = f"h{random.randint(1, 8)}.jpg"
        agent_id = random.randint(1, 2)
        is_rented = random.choice([True, False])
        tenant_id = random.randint(1, 4) if is_rented else None
        return Property(name=name, description=description, address=address, price=price, bedrooms=bedrooms, bathrooms=bathrooms, square_meters=square_meters, image=image, agent_id=agent_id, is_rented=is_rented, tenant_id=tenant_id)

def create_random_houses(app):
    """Create random houses."""
    with app.app_context():
        # Get the number of houses with no tenant
        num_houses = Property.query.filter_by(tenant_id=None).count()

        # Create random houses
        for i in range(num_houses, num_houses + 8):
            house = generate_random_house(app)
            db.session.add(house)

        db.session.commit()
        print("Created random houses!")

